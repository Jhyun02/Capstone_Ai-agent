# MCP SQL Chatbot & Dashboard

A Streamlit application that allows users to interact with an SQL database using natural language and visualize database trends. The application leverages the MCP (Modular Control Protocol) to connect to an SQL server, execute queries, and generate interactive dashboards.

## Features

*   **Natural Language Interface:** Ask questions about your database in plain English.
*   **SQL Query Generation:** Automatically converts natural language questions into SQL queries.
*   **Interactive Dashboard:** Generates visualizations and insights from your database.
*   **Real-time Results:** Get immediate responses to your queries.
*   **Downloadable Dashboards:** Export your dashboards as HTML files.

## Prerequisites

*   Python 3.10 or higher
*   UV package manager
*   Access to a SQL database
*   API key for either OpenAI or Groq

## Environment Variables

Set the following environment variables in a `.env` file in the project root:

*   `MODEL_API_KEY`: Your API key for either OpenAI or Groq
*   `MODEL_ID`: The model ID to use (e.g., "llama-3.3-70b-versatile" for Groq or "gpt-4" for OpenAI)
*   `DB_HOST`: The hostname or IP address of your database server
*   `DB_USER`: The username for your database
*   `DB_PASSWORD`: The password for your database
*   `DB_NAME`: The name of your database

## Setup and Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/vivekpathania/ai-experiments
    cd mcp-agent-experiment
    ```

2.  **Install Dependencies with UV:**

    ```bash
    uv sync
    ```
    This command will:
    * Create a virtual environment if one does not exist
    * Install all the dependencies listed in the `pyproject.toml` file

3.  **Create `.env` File:**

    Create a `.env` file in the project root and add your environment variables:

    ```
    DB_HOST=your_db_host
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name
    MODEL_API_KEY=your_api_key
    MODEL_ID=your_model_id
    ```

## Running the Application

1.  **Activate the Virtual Environment:**
    ```bash
    source .venv/bin/activate  # On Linux/macOS
    .venv\Scripts\activate     # On Windows
    ```

2.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```

3.  **Access the App:**
    Open your web browser and go to the URL provided in the terminal (usually `http://localhost:8501`).

## Usage

### Chatbot Tab

1.  **Ask Questions:** In the "Chatbot" tab, type your questions about the database in natural language (e.g., "List all employees," "What are the top-selling products?").
2.  **View Results:** The chatbot will respond with a natural language summary of the data.

### Dashboard Tab

1.  **Generate Dashboard:** In the "Dashboard" tab, click the "Generate Dashboard" button.
2.  **View Dashboard:** The app will analyze the database schema and generate an interactive HTML dashboard with charts and tables.
3.  **Download Dashboard:** Click the "Download Dashboard HTML" button to save the dashboard as an HTML file.

## Key Components

*   **`agent.py`:**
    *   Defines the agent that handles natural language to SQL conversion
    *   Uses the MCP toolkit to interact with the SQL database
    *   Implements async operations for efficient database communication
    *   Returns natural language summaries of query results

*   **`dashboard_agent.py`:**
    *   Handles dashboard generation and visualization
    *   Analyzes database schema to identify key metrics
    *   Generates appropriate visualizations based on data types
    *   Creates interactive HTML dashboards using Chart.js and Tailwind CSS

*   **`app.py`:**
    *   Main Streamlit application
    *   Provides the user interface for both chatbot and dashboard
    *   Manages async operations using a persistent event loop
    *   Handles session state and user interactions

## Technical Details

*   **Async Operations:** The application uses Python's asyncio for efficient database operations
*   **Event Loop Management:** A persistent event loop is maintained for Streamlit compatibility
*   **MCP Integration:** Uses the latest MCP library for SQL server communication
*   **Model Support:** Compatible with both OpenAI and Groq language models

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

MIT
