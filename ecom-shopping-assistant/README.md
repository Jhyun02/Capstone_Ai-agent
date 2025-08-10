# AI-Powered E-commerce Shopping Assistant

This project is an AI-powered e-commerce shopping assistant that helps users find and compare products effortlessly. It leverages large language models (LLMs), web search tools, and web scraping to provide a seamless shopping experience.

### **Demo**
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ecom-shopping-assistant.streamlit.app/)



## Features

-   **Conversational Interface:** Interact with the AI assistant through a natural language chat interface.
-   **Product Category Identification:** The assistant can identify the product category from user input (text or image).
-   **Requirement Extraction:** It engages in a conversation to extract specific product requirements (e.g., budget, features, brand, size, color).
-   **Image-Based Search:** Users can upload images, and the AI will identify the product and generate a text query.
-   **Enhanced Search Queries:** The assistant refines user queries to improve search results.
-   **Web Search and Scraping:** It uses web search tools (Tavily or SerpApi) to find relevant product links and then scrapes product details from e-commerce websites.
-   **Product Comparison:** The AI generates a visually appealing HTML-based comparison of the found products.
- **Multiple Search Tool Support**: Supports Tavily and SerpApi search tools.
- **Firecrawl**: Uses Firecrawl for web scraping.
- **Streamlit**: Uses Streamlit for the user interface.

## Project Structure

The project is organized into several key components:

-   **`app.py`:** The main Streamlit application that handles user interaction and orchestrates the workflow.
-   **`conversation.py`:** Contains the `ConversationAgent` and `CategoryIdentification` classes for conversational requirement extraction.
-   **`shopping_team.py`:** Contains the `ShoppingTeam` workflow, which manages the search, scraping, and comparison agents.
-   **`image_processing.py`:** Contains the `ProductImageProcessingAgent` for image-based product identification.
-   **`utils.py`:** Utility functions for getting models and search tools.
-   **`instructions.py`:** Contains the instructions for the different agents.
-   **`expCrawl.py`:** A file for testing the `product_comparison_agent`.
- **`travel-agent`**: A folder containing the code for a travel agent.
- **`hrapp`**: A folder containing the code for a HR app.

## Setup Instructions

1.  **Clone the Repository:**

    ```bash
    git clone clone https://github.com/vivekpathania/ai-experiments
    cd ecom-shopping-assistant
    ```

2.  **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application:**

    ```bash
    streamlit run app.py
    ```

    This will start the Streamlit application, and you can access it in your web browser at `http://localhost:8501`.

## Usage

1.  **Set API Keys:**
    -   In the sidebar, select the LLM provider OpenAI and the search tool (Tavily or SerpApi).
    -   Enter your API keys for the selected services.
    -   Click "Set keys".

2.  **Start a Conversation:**
    -   In the chat input, type your product search query (e.g., "I'm looking for a blue denim jeans under $100").
    -   The AI assistant will engage in a conversation to gather more details.
    - You can also upload an image to search for a product.

3.  **View Product Comparison:**
    -   Once the AI has enough information, it will fetch product recommendations and display a comparison in HTML format.

4. **Clear Conversation**:
    - You can clear the conversation by clicking on the "Clear Conversation" button in the sidebar.

## Code Overview

-   **`app.py`:**
    -   Handles the Streamlit UI.
    -   Manages session state.
    -   Orchestrates the `ConversationAgent` and `ShoppingTeam`.
    -   Handles image uploads and calls the `ProductImageProcessingAgent`.
-   **`conversation.py`:**
    -   **`CategoryIdentification`:** Identifies the product category and extracts initial requirements.
    -   **`ConversationAgent`:** Engages in a conversation with the user to gather more details.
-   **`shopping_team.py`:**
    -   **`ShoppingTeam`:** A workflow that orchestrates the following agents:
        -   **`site_finder`:** Enhances the search query and identifies relevant e-commerce sites.
        -   **`researcher`:** Searches for product links on the identified sites.
        -   **`scraping_agent`:** Scrapes product details from the links.
        -   **`product_comparison_agent`:** Generates the HTML comparison layout.
-   **`image_processing.py`:**
    -   **`ProductImageProcessingAgent`:** Identifies the product in an image and generates a text query.
-   **`utils.py`:**
    -   **`getModel()`:** Returns the appropriate LLM model based on the selected mode.
    -   **`getSearchTool()`:** Returns the selected search tool.
-   **`instructions.py`:**
    -   Contains the instructions for each agent, defining their roles and behavior.
- **`expCrawl.py`**:
    - A file for testing the `product_comparison_agent`.
- **`travel-agent`**:
    - A folder containing the code for a travel agent.
- **`hrapp`**:
    - A folder containing the code for a HR app.

## Contributing

Contributions are welcome! If you find a bug or want to add a new feature, please open an issue or submit a pull request.

## License

This project is licensed under the Apache License.

## Acknowledgments
- [Streamlit](https://streamlit.io)
- [OpenAI](https://platform.openai.com/)
- [Tavily](https://tavily.com)
- [SerpApi](https://serpapi.com)
- [Firecrawl](https://www.firecrawl.dev/)


