from pydantic import BaseModel, Field
from typing import List

class StoryPage(BaseModel):
    """Represents a single page of the story"""
    page_number: int = Field(..., description="The page number in the story")
    content: str = Field(..., description="The story content for this page")
    image_prompt: str = Field(..., description="A detailed prompt for generating an image for this page")

class StoryOutput(BaseModel):
    """The complete story output with pages and image prompts"""
    title: str = Field(..., description="The title of the story")
    pages: List[StoryPage] = Field(..., description="List of story pages with their content and image prompts")
    moral: str = Field(..., description="The moral or lesson of the story")
    age_group: str = Field(..., description="The target age group for the story")
    word_count: int = Field(..., description="Total word count of the story") 