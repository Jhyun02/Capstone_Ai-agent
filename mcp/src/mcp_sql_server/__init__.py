"""
mcp_sql_server package.

This package provides a read-only MCP server for interacting with MySQL databases.
"""
from . import server
import asyncio
import argparse


def main():
    """
    Main entry point for the mcp_sql_server package.

    Parses command-line arguments and starts the MCP SQL server.
    """
    parser = argparse.ArgumentParser(description='MySql MCP Server (read-only)')

    parser.add_argument('--db-host',
                        help='Databse url to connect to', required=True)
    parser.add_argument('--db-user',
                        help='DB user', required=True)
    parser.add_argument('--db-password',
                        help='DB password', required=True)
    parser.add_argument('--db-database',
                        help='Database name', required=True)

    args = parser.parse_args()
    print(args)
    asyncio.run(server.main(args.db_host, args.db_user, args.db_password, args.db_database))


# Optionally expose other important items at package level
__all__ = ["main", "server"]

if __name__ == "__main__":
    main()
