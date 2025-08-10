from agno.models.groq import Groq
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.utils.log import logger
import os
from dotenv import load_dotenv
load_dotenv()
model_id = os.getenv("MODEL_ID")
if not model_id:
        raise ValueError("MODEL_ID environment variable is not set.")
api_key = os.getenv("MODEL_API_KEY")
if not api_key:
        raise ValueError("MODEL_API_KEY environment variable is not set.")


def get_model():

    logger.info(f"Using model: {model_id}")
    if 'gpt' in  model_id.lower():
        return OpenAIChat(id=model_id,api_key=api_key)
    if 'claude' in  model_id.lower():
        return Claude(id=model_id,api_key=api_key)

    return Groq(id=model_id,api_key=api_key)
