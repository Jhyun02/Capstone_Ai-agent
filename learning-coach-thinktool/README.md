<div align="center">

# 🎓 Learning Coach

### Your AI-Powered Learning Journey Companion

*Generate personalized learning curricula and discover high-quality learning resources with AI*

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![UV Package Manager](https://img.shields.io/badge/Package%20Manager-UV-blueviolet)](https://github.com/astral-sh/uv)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## 🌟 Overview

Learning Coach is an intelligent AI-powered system that analyzes user learning goals and creates optimized learning plans. Using advanced reasoning capabilities inspired by Agno's think tool approach, it determines the appropriate learning duration (defaulting to 12 weeks if not specified) and generates personalized learning experiences through two specialized agents:

- 📚 **CurriculumAgent**: Analyzes learning goals and user-specified timeframes to create structured learning curricula
- 🔍 **ResourceAgent**: Discovers and recommends high-quality learning resources for each topic

## ✨ Features

- 🎯 **Smart Duration Analysis**: Intelligently determines required learning duration based on goals and complexity
- ⏰ **Flexible Timeframes**: Adheres to user-specified learning durations when provided
- 📚 **Curated Resources**: High-quality learning materials for each topic
- 🎨 **Resource Diversity**: Mix of videos, articles, courses, and documentation
- 🛠️ **Project-Based Learning**: Hands-on projects to reinforce concepts
- 📈 **Progressive Learning**: Structured advancement from basics to advanced topics
- 🤔 **Enhanced Reasoning**: Utilizes think tool methodology for improved learning path analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- UV package manager (faster & more secure alternative to pip)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vivekpathania/ai-experiments/tree/main/learning-coach-thinktool
    cd learning-coach
    ```

2.  **Install Dependencies with UV:**
    Make sure you have UV installed (see Prerequisites). Then run:
    ```bash
    uv sync
    ```
    This command will automatically:
    *   Create a virtual environment (`.venv`) in the project directory if one doesn't exist.
    *   Install all the necessary dependencies listed in `pyproject.toml` (or `requirements.txt`) into the virtual environment.

3.  **Configure environment variables:**
    Copy the example environment file:
    ```bash
    cp env.example .env
    ```
    Then, edit the `.env` file and add your credentials:
    
    *   `MODEL_API_KEY`: Your API key. Supports OPENAI, GROQ, CLAUDE  
    *   `MODEL_ID`: Preferred model (e.g. `meta-llama/llama-4-scout-17b-16e-instruct`, gpt-4o, etc).


## 💻 Usage

### Using the Streamlit Interface

Launch the user-friendly web interface:

```bash
streamlit run streamlit_ui/frontend.py
```

## 📝 Project Structure

```
learning-coach/
├── agents/              # AI agents for curriculum and resource discovery
│   ├── learning_curriculum_workflow.py
│   └── resource_agent.py
    └── curriculum_agent.py
├── streamlit_ui/        # Web interface
│   └── frontend.py
├── utils/              # Utility functions
│   └── llm.py
├── pyproject.toml      # Project dependencies and metadata
├── uv.lock             # UV dependency lock file
└── .env                # Environment variables
```

## 💪 Why UV?

This project uses UV instead of pip for package management because:

- 🚀 **Faster Installation**: UV is significantly faster than pip
- 🔒 **Better Security**: Built-in security features and improved dependency resolution
- 📌 **Reproducible Builds**: Precise dependency locking with uv.lock
- 🧲 **Modern Python**: Native support for modern Python packaging standards

## 📖 Documentation

For detailed documentation on using Learning Coach's features:

1. **Curriculum Generation**
   - Specify your learning goal and optional timeframe
   - Get an intelligently structured learning plan
   - Review and customize the curriculum

## 🤔 Think Tool Integration

Learning Coach leverages the power of think tool methodology, as popularized by Agno and Anthropic, to enhance its reasoning capabilities. This approach provides:

- 🧠 **Structured Analysis**: Dedicated reasoning space for analyzing learning requirements
- ⚖️ **Duration Assessment**: Smart evaluation of required learning time
- 🎯 **Goal Decomposition**: Breaking down learning objectives into manageable chunks

2. **Resource Discovery**
   - Access curated learning materials
   - Filter by content type and difficulty
   - Track your progress

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Thanks to [Groq](https://groq.com/) for their powerful LLM API
- Built with [Streamlit](https://streamlit.io/) for the web interface
- Package management by [UV](https://github.com/astral-sh/uv)
- Agno for building teh agent  [AGNO](https://agno.com)
```

This will:
1. Start a web interface where you can input your learning goal
2. Generate a 12-week curriculum for your topic
3. Find relevant resources for each week
4. Save the complete curriculum with resources to a JSON file


#### Features

- **Understands Weekly Topics**: Takes input from the CurriculumAgent about weekly topics, concepts, and projects.
- **Finds High-Quality Resources**: Searches for the best learning resources that explain or teach the week's topics.
- **Categorizes Resources**: Labels each resource with title, URL, type, cost, and estimated time.
- **Ensures Relevance**: Matches resources tightly to the week's learning objectives.
- **Avoids Redundancy**: Prioritizes fresh resources each week.
- **Diversifies Resource Formats**: Provides different formats to accommodate different learning styles.
- **Respects Learning Level**: Adapts suggestions based on the implied experience level.

#### Resource Types

The ResourceAgent finds various types of learning resources:

- Videos (YouTube, course previews)
- Articles and blogs
- Full-length courses (Coursera, Udemy, etc.)
- Official documentation or GitHub repos
- Tutorials or walkthroughs for projects

#### Output Format

The ResourceAgent returns structured data for each week:

```json
{
  "week": 4,
  "resources": [
    {
      "title": "Mastering Flutter Navigation",
      "url": "https://www.udemy.com/course/flutter-navigation",
      "type": "video-course",
      "cost": "paid"
    },
    {
      "title": "Official Docs: Navigator 2.0",
      "url": "https://flutter.dev/docs/development/ui/navigation",
      "type": "documentation",
      "cost": "free"
    },
    {
      "title": "Flutter Navigation Deep Dive",
      "url": "https://medium.com/flutter/navigation-101",
      "type": "article",
      "cost": "free"
    }
  ]
}
```


## License

This project is licensed under the MIT License - see the LICENSE file for details.
