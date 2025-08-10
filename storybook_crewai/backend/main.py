import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.agents.story_writing_agent import StoryWritingAgent
from backend.agents.image_agent import ImageGenerationAgent
from backend.audio_generator.elevenlabs_storyteller import StoryAudioGenerator
from backend.movie_generator.movie_compiler import StoryVideoCompiler
from backend.models import StoryOutput

async def generate_story_with_media(prompt: str, max_pages: int = 3) -> str:
    """Generate a complete story with images, audio, and video."""
    try:
        # Create output directories
        output_dir = project_root / "output"
        images_dir = output_dir / "images"
        audio_dir = output_dir / "audio"
        
        for dir_path in [output_dir, images_dir, audio_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
        
        # Step 1: Generate the story
        print("Generating story...")
        story_agent = StoryWritingAgent()
        story_output, metadata = story_agent.write_story(
            prompt=prompt,
            max_pages=max_pages
        )
        
        print(f"Story generated: {story_output.title}")
        
        # Step 2: Generate images
        print("\nGenerating images...")
        image_agent = ImageGenerationAgent()
        image_paths = await image_agent.generate_images(story_output, str(images_dir))
        print(f"Generated {len(image_paths)} images")
        
        # Verify all images were generated
        for page in story_output.pages:
            image_path = images_dir / f"page_{page.page_number}_{story_output.title.lower().replace(' ', '_')}.png"
            if not image_path.exists():
                raise FileNotFoundError(f"Image not generated for page {page.page_number}")
        
        # Step 3: Generate audio
        print("\nGenerating audio...")
        audio_generator = StoryAudioGenerator(output_dir=audio_dir)
        audio_paths = await audio_generator.generate_story_audio(story_output)
        print(f"Generated {len(audio_paths)} audio files")
        
        # Verify all audio files were generated
        for page in story_output.pages:
            audio_path = audio_dir / f"page_{page.page_number}_{story_output.title.lower().replace(' ', '_')}.mp3"
            if not audio_path.exists():
                raise FileNotFoundError(f"Audio not generated for page {page.page_number}")
        
        # Step 4: Compile the video
        print("\nCompiling video...")
        video_compiler = StoryVideoCompiler(output_dir=output_dir)
        video_path = video_compiler.compile_story_video(story_output)
        
        print(f"Video created successfully: {video_path}")
        
        return video_path
        
    except Exception as e:
        print(f"Error in story generation process: {str(e)}")
        raise

async def main():
    # Load environment variables
    load_dotenv()
    
    # Get user input
    prompt = input("Enter your story prompt: ")
    max_pages = input("Enter maximum number of pages (default: 3): ")
    max_pages = int(max_pages) if max_pages.strip() else 3
    
    try:
        # Generate the complete story with media
        video_path = await generate_story_with_media(prompt, max_pages)
        print(f"\nStory generation complete! Video saved at: {video_path}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 