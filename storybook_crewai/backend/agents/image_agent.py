from crewai import Agent, Task, Crew, LLM
from crewai_tools import DallETool
import os
import sys
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path
from typing import List
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

from backend.models import StoryOutput, StoryPage
import json
import requests
from PIL import Image
from io import BytesIO
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Load environment variables
load_dotenv()

class ImageGenerationAgent:
    def __init__(self):
        self.model = os.getenv("IMAGE_MODEL", "dall-e-3")
        self.temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
        self.api_key = os.getenv("OPENAI_API_KEY")
       
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.image_agent = self.__createAgent()
        self.executor = ThreadPoolExecutor(max_workers=3)  # Limit concurrent image generations

    def __createAgent(self) -> Agent:
        llm = LLM(
            model="gpt-4",  # Using GPT-4 for prompt refinement
            temperature=self.temperature,
            api_key=self.api_key
        )

        # Configure DALL-E tool with specific parameters
        dalle_tool = DallETool(
            model="dall-e-3",
            size="1024x1024",
            quality="standard",
            n=1
        )

        return Agent(
            role="Children's Story Illustrator",
            goal="Generate colorful, cartoonish images for children's story pages",
            backstory="""You are a talented children's book illustrator with expertise in creating 
            colorful, cartoonish images that appeal to children. You excel at transforming story 
            prompts into engaging visual scenes that capture the essence of each page while maintaining 
            a consistent style throughout the story.""",
            llm=llm,
            tools=[dalle_tool],
            verbose=True
        )

    async def _generate_image(self, prompt: str, output_path: str) -> str:
        """Generate an image using CrewAI's DALL-E tool"""
        try:
            # Create a task for refining the prompt and generating the image
            task = Task(
                description=f"""Generate a colorful, cartoonish illustration for a children's story page.
                
                Scene description: {prompt}
                
                Requirements:
                1. Style: Colorful and cartoonish
                2. Mood: Positive and engaging
                3. Detail: Clear and easy to understand
                4. Characters: Expressive and friendly
                5. Colors: Bright and vibrant
                
                The image should be suitable for children and capture the essence of the story page.
                
                IMPORTANT: Use the DALL-E tool to generate the image and return ONLY the image URL.
                Do not include any other text or explanation in your response.""",
                expected_output="The URL of the generated image, nothing else",
                agent=self.image_agent
            )
            
            # Create a crew with just the image agent
            crew = Crew(
                agents=[self.image_agent],
                tasks=[task],
                verbose=True
            )
            
            # Execute the task in a thread pool
            loop = asyncio.get_event_loop()
            crew_output = await loop.run_in_executor(
                self.executor,
                crew.kickoff
            )
            
            # Extract the actual output from the CrewOutput object
            if hasattr(crew_output, 'raw_output'):
                response = str(crew_output.raw_output)
            elif hasattr(crew_output, 'output'):
                response = str(crew_output.output)
            else:
                response = str(crew_output)
            
            # Clean up the response to get just the URL
            if not response:
                raise ValueError("Empty response from agent")
                
            # Remove any surrounding quotes or whitespace
            image_url = response.strip().strip('"\'')
            
            # Validate it's a DALL-E URL
            if not image_url.startswith('https://oaidalleapiprodscus.blob.core.windows.net'):
                raise ValueError(f"Invalid DALL-E URL format: {image_url}")
            
            # Download the image from the URL
            response = requests.get(image_url)
            if response.status_code != 200:
                raise ValueError(f"Failed to download image: {response.text}")
            
            # Save the image
            image = Image.open(BytesIO(response.content))
            image.save(output_path)
            
            return output_path
            
        except Exception as e:
            raise ValueError(f"Failed to generate image: {str(e)}")

    async def generate_images(self, story: StoryOutput, output_dir: str) -> List[str]:
        """Generate images for all pages in the story asynchronously"""
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Create tasks for all images
        tasks = []
        for page in story.pages:
            # Create a unique filename for each page
            filename = f"page_{page.page_number}_{story.title.lower().replace(' ', '_')}.png"
            output_path = os.path.join(output_dir, filename)
            
            # Create task for this page's image
            task = self._generate_image(page.image_prompt, output_path)
            tasks.append(task)
        
        # Wait for all images to be generated
        generated_images = []
        for i, task in enumerate(tasks, 1):
            try:
                image_path = await task
                generated_images.append(image_path)
                print(f"Generated image for page {i}: {image_path}")
            except Exception as e:
                print(f"Error generating image for page {i}: {str(e)}")
        
        return generated_images

    def __del__(self):
        """Clean up the thread pool executor"""
        self.executor.shutdown(wait=True)
