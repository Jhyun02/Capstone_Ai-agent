from crewai import Agent, Task, Crew, LLM
import glob
import json
import os
from cache.prompt_cache import load_response, save_response, get_cache_stats
from dotenv import load_dotenv
from datetime import datetime


# Load environment variables
load_dotenv()

class ELI5Agent:
    def __init__(self):
        self.model = os.getenv("AGENT_MODEL", "gpt-4")
        self.temperature = float(os.getenv("AGENT_TEMPERATURE", "0.7"))
        self.api_key = os.getenv("MODEL_API_KEY")
        self.cache_enabled = os.getenv("CACHE_ENABLED", "True").lower() == "true"
        if not self.api_key:
            raise ValueError("MODEL_API_KEY not found in environment variables")

    def __createAgent(self) -> Agent:
        llm = LLM(
            model=self.model,
            temperature=self.temperature,
            api_key=self.api_key
        )
        return Agent(
            role="AI Tutor",
            goal="Explain complex things in simple, child-friendly terms",
            backstory="You're an expert educator who explains hard things like you're talking to a curious 5-year-old.",
            llm=llm,
            verbose=True
        )

    def __createTask(self, agent: Agent) -> Task:
        return Task(
            description="Answer the user's question {question} in a way that is easy to understand",
            expected_output="A simple, child-friendly explanation of the user's prompt",
            agent=agent,
        )


    def _extract_response_text(self, crew_output) -> str:
        """Extract the text content from a CrewOutput object."""
        if hasattr(crew_output, 'raw_output'):
            return str(crew_output.raw_output)
        elif hasattr(crew_output, 'output'):
            return str(crew_output.output)
        return str(crew_output)

    def explain(self, user_prompt: str) -> tuple[str, dict]:
        # Check cache first
        if self.cache_enabled:
            cached_response = load_response(user_prompt)
            if cached_response:
                return cached_response["response"], {
                    "cached": True,
                    "model": self.model,
                    "temperature": self.temperature,
                    "timestamp": cached_response.get("timestamp", datetime.now().isoformat())
                }

        # Create agent and task
        agent = self.__createAgent()
        task = self.__createTask(agent)
        crew = Crew(
            agents=[agent],
            tasks=[task],
            verbose=True
        )

        # Get response
        crew_output = crew.kickoff({"question": user_prompt})
        
        # Extract the text content from the CrewOutput
        response_text = self._extract_response_text(crew_output)

        # Prepare metadata
        metadata = {
            "cached": False,
            "model": self.model,
            "temperature": self.temperature,
            "timestamp": datetime.now().isoformat()
        }

        # Cache the response if enabled
        if self.cache_enabled:
            save_response(user_prompt, response_text, metadata)

        return response_text, metadata

    def get_cache_info(self) -> dict:
        """
        Get information about the cache.
        
        Returns:
            dict: Dictionary containing cache statistics including:
                - total_entries: Number of cached responses
                - total_size_bytes: Total size of cache in bytes
                - oldest_entry: Timestamp of oldest cached response
                - newest_entry: Timestamp of newest cached response
        """
        return get_cache_stats()
