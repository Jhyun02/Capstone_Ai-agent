from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict
import asyncio
from pathlib import Path
import json
from datetime import datetime

from agents.story_writing_agent import StoryWritingAgent
from agents.image_agent import ImageGenerationAgent
from audio_generator.elevenlabs_storyteller import ElevenLabsStoryteller
from movie_generator.movie_compiler import create_story_video
from models import StoryOutput, StoryPage

app = FastAPI(
    title="Storybook Generator API",
    description="API for generating children's stories with images, audio narration, and video compilation",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StoryRequest(BaseModel):
    prompt: str
    max_pages: Optional[int] = 3

class StoryResponse(BaseModel):
    title: str
    pages: List[dict]
    moral: str
    age_group: str
    word_count: int
    metadata: dict

class CompileRequest(BaseModel):
    story: StoryResponse
    background_music: Optional[bool] = True
    voice_id: Optional[str] = "21m00Tcm4TlvDq8ikWAM"  # Default ElevenLabs voice ID

class CompileResponse(BaseModel):
    status: str
    video_path: Optional[str]
    error: Optional[str]
    progress: Dict[str, str]

# Store compilation progress
compilation_progress = {}

async def compile_storybook(story: StoryResponse, background_music: bool, voice_id: str, task_id: str):
    try:
        # Update progress
        compilation_progress[task_id] = {"status": "starting", "message": "Initializing compilation"}
        
        # 1. Generate images
        compilation_progress[task_id] = {"status": "generating_images", "message": "Generating images for each page"}
        image_agent = ImageGenerationAgent()
        await image_agent.generate_images(story)
        
        # 2. Generate audio
        compilation_progress[task_id] = {"status": "generating_audio", "message": "Generating audio narration"}
        audio_generator = ElevenLabsStoryteller()
        await audio_generator.generate_audio(story, voice_id)
        
        # 3. Compile video
        compilation_progress[task_id] = {"status": "compiling_video", "message": "Creating final video"}
        video_path = await create_story_video(story, background_music)
        
        # Update final status
        compilation_progress[task_id] = {
            "status": "completed",
            "message": "Storybook compilation completed",
            "video_path": video_path
        }
        
    except Exception as e:
        compilation_progress[task_id] = {
            "status": "error",
            "message": str(e)
        }

@app.get("/")
async def root():
    return {"message": "Welcome to Storybook Generator API"}

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        # Initialize the story writing agent
        story_agent = StoryWritingAgent()
        
        # Generate the story
        story_output, metadata = story_agent.write_story(
            prompt=request.prompt,
            max_pages=request.max_pages
        )
        
        # Convert the story output to a dictionary
        story_dict = {
            "title": story_output.title,
            "pages": [page.dict() for page in story_output.pages],
            "moral": story_output.moral,
            "age_group": story_output.age_group,
            "word_count": story_output.word_count,
            "metadata": metadata
        }
        
        return story_dict
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compile-storybook", response_model=CompileResponse)
async def compile_storybook_endpoint(request: CompileRequest, background_tasks: BackgroundTasks):
    try:
        # Generate a unique task ID
        task_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Start compilation in background
        background_tasks.add_task(
            compile_storybook,
            request.story,
            request.background_music,
            request.voice_id,
            task_id
        )
        
        return {
            "status": "started",
            "task_id": task_id,
            "message": "Storybook compilation started"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/compilation-status/{task_id}")
async def get_compilation_status(task_id: str):
    if task_id not in compilation_progress:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return compilation_progress[task_id]

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 