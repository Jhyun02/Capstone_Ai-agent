# ELI5 Tutor with Prompt Caching

A Streamlit-based application that provides simple, easy-to-understand explanations using AI, with an efficient prompt caching system to improve response times and reduce API calls.

## Features

- 🤖 AI-powered explanations using CrewAI
- 💾 Smart prompt caching with semantic search
- 🔍 Semantic similarity matching for cached responses
- 📊 Cache statistics and monitoring
- 🎨 Clean, modern UI with Streamlit

## Installation

This project uses `uv` for dependency management. To get started:

1. Clone the repository:
```bash
git clone https://github.com/vivekpathania/ai-experiments
cd prompt_caching
```

2. Install dependencies using `uv`:
```bash
uv sync
```

3. Create a `.env` file with your API credentials:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Project Structure

```
prompt_caching/
├── src/
│   ├── agents/
│   │   └── eli5_agent.py      # ELI5 agent implementation
│   ├── cache/
│   │   └── prompt_cache.py    # Caching system implementation
│   └── main.py                # Main application entry point
│   └── app.py                # Streamlit app
├── .env.example              # Example environment variables
└── README.md                # Project documentation
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py.py
```

2. Access the application at `http://localhost:8501`

3. Enter your questions and get simple explanations

## Features in Detail

### Prompt Caching
- Efficient storage of responses using JSON files
- Semantic search for similar queries
- Cache statistics and monitoring
- Automatic cache cleanup

### ELI5 Agent
- Uses CrewAI for generating explanations
- Configurable model and temperature
- Metadata tracking for responses
- Support for different explanation styles

### UI Features
- Clean, modern interface
- Real-time response display
- Cache statistics visualization
- Easy-to-use controls

## Development


### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Include docstrings for all functions and classes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details
