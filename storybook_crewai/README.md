# Storybook CrewAI

A Python project that generates children's storybooks with images, audio narration, and video compilation using AI agents.

## Features

- Story generation using CrewAI agents
- Image generation using DALL-E
- Audio narration using ElevenLabs
- Video compilation with MoviePy
- Sequential processing of story assets
- Async operations for better performance

## Prerequisites

- Python 3.9+
- UV package manager (instead of pip)
- OpenAI API key
- ElevenLabs API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vivekpathania/ai-experiments
cd storybook-crewai
```

2. Install dependencies using UV:
```bash
uv sync
```

3. Copy the environment file and add your API keys:
```bash
cp .env.example .env
```

## Environment Variables

Create a `.env` file with the following variables:
```
OPENAI_API_KEY=your_openai_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
IMAGE_MODEL=dall-e-3
AGENT_TEMPERATURE=0.7
```

## Project Structure

```
storybook_crewai/
├── backend/
│   ├── agents/
│   │   ├── story_writing_agent.py
│   │   └── image_agent.py
│   ├── audio_generator/
│   │   └── elevenlabs_storyteller.py
│   ├── movie_generator/
│   │   └── movie_compiler.py
│   ├── models.py
│   └── main.py
├── output/
│   ├── images/
│   ├── audio/
│   └── videos/
├── .env.example
└── README.md
```

## Usage

1. Run the main script:
```bash
python uv run backend/main.py
```

2. Follow the prompts:
   - Enter your story prompt
   - Specify the number of pages (default: 3)

3. The script will:
   - Generate the story
   - Create images for each page
   - Generate audio narration
   - Compile everything into a video

## Output

The generated files will be saved in the `output` directory:
- Images: `output/images/page_{number}_{title}.png`
- Audio: `output/audio/page_{number}_{title}.mp3`
- Video: `output/{title}.mp4`

## Development

### Using UV

This project uses UV instead of pip for package management. Key UV commands:

```bash
# Install dependencies
uv sync

# Add a new package
uv pip install package_name

# Update dependencies
uv pip install --upgrade package_name

# Create requirements.txt
uv pip freeze > requirements.txt
```

### Adding New Features

1. Create new agent classes in the `agents` directory
2. Add new generators in their respective directories
3. Update the main flow in `main.py`

## Error Handling

The project includes error handling for:
- Missing API keys
- Failed image generation
- Failed audio generation
- Missing assets during video compilation

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
