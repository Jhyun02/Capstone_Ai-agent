# app.py
import os
from dotenv import load_dotenv
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables import RunnableMap
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
import plotly.express as px
import pandas as pd
from sqlalchemy import text

# Configure Streamlit page
st.set_page_config(
    page_title="Chat with SQL",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="collapsed",
)
load_dotenv()
# Initialize database connection using environment variables
db_uri = "sqlite:///sample.db"

db = SQLDatabase.from_uri(db_uri)

# Initialize Groq LLM with environment variable
groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatOllama(
    model="mistral",
    temperature=0
)

# Get schema of the database
def get_schema(_):
    """Retrieve schema information for all tables in the database."""
    return db.get_table_info()

# Execute SQL query
def run_query(query):
    try:
        with db._engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()

            # 단일 행 단일 열 → 숫자만 있는 경우
            if len(rows) == 1 and len(columns) == 1:
                df = pd.DataFrame(rows, columns=columns)
                return df  # or rows[0][0] if just the number is needed
            # 여러 행 or 여러 열인 경우
            elif rows:
                df = pd.DataFrame(rows, columns=columns)
                return df
            else:
                return pd.DataFrame(columns=columns)
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
template_final = """
You are an AI assistant that converts SQL query results into natural language answers.

Here is the table schema:
{schema}

Question: {question}
SQL Query: {query}
SQL Response: {response}

Instructions:
- Use the exact data from the SQL Response.
- If the response is a number (e.g., [(10000,)]), use it directly in the answer.
- If the response includes multiple rows (e.g., [('Sales', 200), ('HR', 100)]), summarize each row.
- Do not guess or infer anything that is not in the SQL result.
- Answer in one clear and complete English sentence.

Answer:
"""

# 시각화 조건 판별
def is_visualizable(df: pd.DataFrame) -> bool:
    return df is not None and not df.empty and df.select_dtypes(include='number').shape[1] >= 1

# 시각화 함수
def visualize_df(df: pd.DataFrame):
    st.subheader("📊 Visualization (Beta)")

    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    category_cols = df.select_dtypes(exclude='number').columns.tolist()

    if numeric_cols and category_cols:
        x_col = st.selectbox("Select X-axis (Category)", category_cols)
        y_col = st.selectbox("Select Y-axis (Numeric)", numeric_cols)
        chart_type = st.selectbox("Chart Type", ["Bar", "Line", "Pie"])

        if chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col)
        elif chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col)
        elif chart_type == "Pie":
            fig = px.pie(df, names=x_col, values=y_col)

        st.plotly_chart(fig)
    else:
        st.info("Not enough data for visualization.")

prompt_response = ChatPromptTemplate.from_template(template_final)

# Full chain to execute query and generate response
full_chain = (
    RunnablePassthrough.assign(
        schema=get_schema,
        query=sql_chain
    )
    .assign(
        response=lambda x: run_query(x["query"]),
    )
    | RunnableMap({  # 여러 항목을 동시에 출력하는 체인 구성
        "query": lambda x: x["query"],
        "response": lambda x: x["response"],
        "final": (
            prompt_response
            | llm
            | StrOutputParser()
        )
    })
)

# Streamlit UI
st.title("Chat with SQL 🧊")
st.write("Ask questions about your database!")

# Chat input
prompt = st.chat_input("What would you like to know?")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = full_chain.invoke({"question": prompt})

                sql_query = result["query"]
                sql_result = result["response"]
                final_answer = result["final"]

                st.subheader("Generated SQL Query")
                st.code(sql_query)

                st.subheader("SQL Result")
                if isinstance(sql_result, pd.DataFrame):
                    if sql_result.empty:
                        st.warning("쿼리 결과가 없습니다.")
                    elif sql_result.shape == (1, 1):
                        st.success(f"Result: {sql_result.iloc[0, 0]}")
                    else:
                        st.dataframe(sql_result)
                        if is_visualizable(sql_result):
                            visualize_df(sql_result)
                else:
                    st.error(sql_result)

                st.subheader("Final Answer")
                st.write(final_answer)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")