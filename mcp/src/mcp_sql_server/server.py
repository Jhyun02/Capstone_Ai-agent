import pymysql
import json
import psycopg2
import logging
from contextlib import closing
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from typing import Any, Literal

logger = logging.getLogger('mcp_sql_server')
logger.info("Starting MCP SQL Server")


class SqlReadOnlyServer:
    """
    A read-only server for interacting with MySQL or PostgreSQL databases.

    This class provides methods to execute SELECT queries and retrieve schema information.
    """

    def __init__(self, host: str, user: str, password: str, database: str, db_type: Literal["mysql", "postgres"] = "mysql", port: str = None):
        """
        Initializes the SqlReadOnlyServer with database connection details.

        Args:
            host (str): The database host address.
            user (str): The database username.
            password (str): The database password.
            database (str): The name of the database.
            db_type (str): Type of database ("mysql" or "postgres")
            port (str): Database port (required for PostgreSQL)
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.db_type = db_type
        self.port = port

        if db_type == "postgres" and not port:
            raise ValueError("Port is required for PostgreSQL connection")

    def _get_schema_for_llm(self) -> str:
        """
        Retrieves the schema information for the database in a format suitable for LLMs.

        Returns:
            str: A JSON string representing the database schema.
        """
        if self.db_type == "mysql":
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            
            schema = {}
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT 
                        TABLE_NAME, 
                        COLUMN_NAME, 
                        DATA_TYPE, 
                        COLUMN_TYPE,
                        IS_NULLABLE, 
                        COLUMN_DEFAULT, 
                        COLUMN_KEY, 
                        EXTRA
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_SCHEMA = %s
                    ORDER BY TABLE_NAME, ORDINAL_POSITION;
                    """
                    cursor.execute(query, (self.database,))
                    results = cursor.fetchall()

                    for row in results:
                        table_name = row[0]
                        column_info = {
                            "name": row[1],
                            "data_type": row[2],
                            "column_type": row[3],
                            "is_nullable": row[4],
                            "default": row[5],
                            "key": row[6],
                            "extra": row[7]
                        }

                        if table_name not in schema:
                            schema[table_name] = []
                        schema[table_name].append(column_info)
            finally:
                connection.close()

        else:  # postgres
            connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            
            schema = {}
            try:
                with connection.cursor() as cursor:
                    query = """
                    SELECT 
                        table_name,
                        column_name,
                        data_type,
                        is_nullable,
                        column_default,
                        character_maximum_length
                    FROM information_schema.columns
                    WHERE table_schema = 'public'
                    ORDER BY table_name, ordinal_position;
                    """
                    cursor.execute(query)
                    results = cursor.fetchall()

                    for row in results:
                        table_name = row[0]
                        column_info = {
                            "name": row[1],
                            "data_type": row[2],
                            "is_nullable": row[3],
                            "default": row[4],
                            "max_length": row[5]
                        }

                        if table_name not in schema:
                            schema[table_name] = []
                        schema[table_name].append(column_info)
            finally:
                connection.close()

        return json.dumps(schema, indent=2)

    def _execute_query(self, query: str) -> list[dict]:
        """
        Executes a SQL query and returns the results as a list of dictionaries.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a row.

        Raises:
            ValueError: If there is an error executing the query.
        """
        if self.db_type == "mysql":
            connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            try:
                with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(query)
                    results = cursor.fetchall()
                    return results
            finally:
                connection.close()
        else:  # postgres
            connection = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            try:
                with connection.cursor() as cursor:
                    cursor.execute(query)
                    columns = [desc[0] for desc in cursor.description]
                    results = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return results
            finally:
                connection.close()


async def main(host: str, user: str, password: str, database: str, db_type: str = "postgres", port: str = '5432'):
    """
    Main function to start the MCP SQL server.

    Args:
        host (str): The database host address.
        user (str): The database username.
        password (str): The database password.
        database (str): The name of the database.
        db_type (str): Type of database ("mysql" or "postgres")
        port (str): Database port (required for PostgreSQL)
    """
    db = SqlReadOnlyServer(host=host, user=user, password=password, database=database, db_type=db_type, port=port)
    server = Server("mcp-sql-server")

    @server.list_tools()
    async def handle_list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="read_query",
                description="Execute a SELECT query on the SQL database",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "SELECT SQL query to execute"},
                    },
                    "required": ["query"],
                },
            ),
            types.Tool(
                name="get_schema",
                description="Get the schema information for the database",
                inputSchema={
                    "type": "object",
                    "properties": {},
                },
            ),
        ]

    @server.call_tool()
    async def handle_call_tool(
        name: str, arguments: dict[str, Any] | None
    ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
        try:
            if name == "get_schema":
                results = db._get_schema_for_llm()
                return [types.TextContent(type="text", text=str(results))]

            if not arguments:
                raise ValueError("Missing arguments")

            if name == "read_query":
                if not arguments["query"].strip().upper().startswith("SELECT"):
                    raise ValueError("Only SELECT queries are allowed for read_query")
                results = db._execute_query(arguments["query"])
                return [types.TextContent(type="text", text=str(results))]

            else:
                raise ValueError(f"Unknown tool: {name}")

        except Exception as e:
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="sql",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
