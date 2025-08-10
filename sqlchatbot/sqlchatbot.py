# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Configure Streamlit page
st.set_page_config(
    page_title="Chat with SQL",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()
# Initialize database connection using environment variables
db_uri = os.getenv("DB_URI")

db = SQLDatabase.from_uri(db_uri)

# Initialize Groq LLM with environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
    temperature=0,
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile"
)

# Get schema of the database
def get_schema(_):
    """Retrieve schema information for all tables in the database."""
    return db.get_table_info()

# Execute SQL query
def run_query(query):
    """Run a SQL query and return the results."""
    try:
        return db.run(query)
    except Exception as e:
        return f"Error executing query: {str(e)}"

# Template for generating SQL queries
template_sql_query = """Based on the table schema below, write a SQL query that would answer the user's question:
{schema}

Question: {question}
SQL Query:
Do not enclose query in ```sql and do not write preamble or explanation.
You MUST return only a single SQL query."""
prompt_sql_query = ChatPromptTemplate.from_template(template_sql_query)

# Chain to generate SQL queries
sql_chain = (
    RunnablePassthrough.assign(schema=get_schema)  # Pass schema to prompt
    | prompt_sql_query
    | llm
    | StrOutputParser()  # Parse LLM output to string
)

# Template for generating final response
template_final = """Based on the table schema below, question, SQL query, and SQL response, write a natural language response:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}
"""
prompt_response = ChatPromptTemplate.from_template(template_final)

# Full chain to execute query and generate response
full_chain = (
    RunnablePassthrough.assign(query=sql_chain)  # Generate SQL query
    .assign(
        schema=get_schema,  # Pass schema
        response=lambda x: run_query(x["query"]),  # Execute query
    )
    | prompt_response
    | llm
    | StrOutputParser()  # Parse final response
)

# Streamlit UI
st.title("Chat with SQL 🧊")
st.write("Ask questions about your database!")

# Chat input
prompt = st.chat_input("What would you like to know?")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate and display response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = full_chain.invoke({"question": prompt})
                st.write(response)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")