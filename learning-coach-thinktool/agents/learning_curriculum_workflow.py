#!/usr/bin/env python3
"""
Learning Curriculum Workflow - A deterministic, stateful workflow for generating
complete learning curricula with resources, assessments, and coaching content.
"""

import json
import re
from typing import Dict, Iterator, Optional, List, Any
from pathlib import Path

from agno.workflow import Workflow, RunEvent, RunResponse
from agno.agent import Agent
from agno.utils.log import logger
from agno.utils.pprint import pprint_run_response


from agents.curriculum_agent import CurriculumAgent
from agents.resource_agent import ResourceAgent

from utils.llm import get_model



class LearningCurriculumWorkflow(Workflow):
    """
    A workflow for generating learning curricula with resources.
    
    This workflow orchestrates multiple specialized agents to create a comprehensive learning plan:
    1. CurriculumAgent: Generates the overall curriculum structure
    2. ResourceAgent: Finds relevant learning resources for each week
    """
    
    description: str = """
    An intelligent learning curriculum generator that creates comprehensive, well-structured learning plans.
    This workflow orchestrates multiple AI agents to design curricula and find resources. The system excels
    at creating personalized learning experiences that combine structured content with practical resources.
    """
    
    # Initialize the specialized agents
    curriculum_agent: Agent = CurriculumAgent()
    resource_agent: Agent = ResourceAgent()
    
    def __init__(self, session_id: str = None, debug_mode: bool = False):
        """
        Initialize the workflow with optional session ID and debug mode.
        
        Args:
            session_id: Optional session ID for identification
            debug_mode: Whether to enable debug mode
        """
        super().__init__(session_id=session_id, debug_mode=debug_mode)
        logger.info("LearningCurriculumWorkflow initialized")
    
    def run(self, learning_goal: str, use_cache: bool = False) -> RunResponse:
        """
        Run the workflow to generate a complete learning curriculum.
        
        Args:
            learning_goal: The learning goal to generate a curriculum for
            use_cache: Whether to use cached results if available (not used in this simplified version)
            
        Returns:
            Iterator[RunResponse]: Iterator of RunResponse objects containing the generated curriculum
        """
        logger.info(f"Generating complete curriculum for goal: '{learning_goal}'")
        
        # Step 1: Generate the curriculum structure
        logger.info("Step 1: Generating curriculum structure")
        curriculum_response = self.curriculum_agent.run(learning_goal)
        
        if not curriculum_response or not curriculum_response.content:
            return RunResponse(
                content={"error": "Failed to generate curriculum structure"},
                event=RunEvent.workflow_completed
            )
            return
        
        # Extract the curriculum data
        curriculum_data = self._extract_json_from_response(curriculum_response.content)
        if "error" in curriculum_data:
            return RunResponse(
                content={"error": f"Failed to parse curriculum data: {curriculum_data['error']}"},
                event=RunEvent.workflow_completed
            )
            return
        
        # Initialize the complete curriculum data
        complete_curriculum = {
            "curriculum": curriculum_data.get("curriculum", []),
            "resources": {}
        }
        
        # Step 2: Generate resources, assessments, and coaching content for each week
        for week_data in complete_curriculum["curriculum"]:
            week_number = week_data.get("week", 0)
            week_str = str(week_number)
            
            # Skip if we don't have a valid week number
            if not week_number:
                continue
            
            logger.info(f"Processing week {week_number}")
            
            # Step 2a: Generate resources for this week
            logger.info(f"Step 2a: Generating resources for week {week_number}")
            week_input = json.dumps({
                "week": week_number,
                "topics": week_data.get("topics", []),
                "concepts": week_data.get("concepts", [])
            })
            
            resource_response = self.resource_agent.run(week_input)
            if resource_response and resource_response.content:
                resource_data = self._extract_json_from_response(resource_response.content)
                if "resources" in resource_data:
                    complete_curriculum["resources"][week_str] = resource_data
            

        
        # Yield the complete curriculum
        logger.info(f"Complete curriculum -- learningcurriculumworkflow: {complete_curriculum}")
        return RunResponse(content=complete_curriculum, event=RunEvent.workflow_completed)
    
    def _extract_json_from_response(self, response_content: Any) -> Dict:
        """
        Extract JSON content from a response that might contain markdown or other formatting.
        
        Args:
            response_content: The content of the response, which might be a string or a dictionary.
            
        Returns:
            dict: The extracted JSON content, or an error message if extraction failed.
        """
        # If the content is already a dictionary, return it
        if isinstance(response_content, dict):
            return response_content
        
        # If the content is a string, try to extract JSON
        if isinstance(response_content, str):
            try:
                # Try to parse the string as JSON
                return json.loads(response_content)
            except json.JSONDecodeError:
                # If it's not valid JSON, try to extract JSON from markdown
                json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_content, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except json.JSONDecodeError:
                        return {"error": "Failed to parse JSON from response"}
                else:
                    return {"error": "No JSON found in response"}
        
        # If the content is something else, return an error
        return {"error": f"Unexpected response content type: {type(response_content)}"}
    
    def print_curriculum(self, curriculum: Dict):
        """
        Print a curriculum in a formatted way.
        
        Args:
            curriculum: The curriculum to print
        """
        print("\n" + "=" * 80)
        print("COMPLETE LEARNING CURRICULUM")
        print("=" * 80)
        
        # Print the curriculum
        if "curriculum" in curriculum:
            for week_data in curriculum["curriculum"]:
                week_number = week_data.get("week", "Unknown")
                print(f"\nWEEK {week_number}")
                print("-" * 50)
                
                # Print topics and concepts
                print("Topics:")
                for topic in week_data.get("topics", []):
                    print(f"  - {topic}")
                
                print("\nConcepts:")
                for concept in week_data.get("concepts", []):
                    print(f"  - {concept}")
                
                print(f"\nProject: {week_data.get('project', 'No project assigned')}")
                
                # Print resources if available
                if "resources" in curriculum and str(week_number) in curriculum["resources"]:
                    print("\nResources:")
                    for resource in curriculum["resources"][str(week_number)].get("resources", []):
                        print(f"  - {resource.get('title', 'Untitled')} ({resource.get('type', 'Unknown type')})") 
                        print(f"    URL: {resource.get('url', 'No URL')}")
                
                print("-" * 50)
        else:
            print("Curriculum data not found in the response.")
            print("Available keys in response:", list(curriculum.keys()))

# Run the workflow if the script is executed directly
if __name__ == "__main__":
    import sys
    from rich.prompt import Prompt
    
    # Get the learning goal from command line arguments or prompt the user
    if len(sys.argv) > 1:
        learning_goal = " ".join(sys.argv[1:])
    else:
        learning_goal = Prompt.ask(
            "[bold]Enter a learning goal[/bold]",
            default="Learn Flutter app development from beginner to advanced"
        )
    
    # Initialize the workflow
    workflow = LearningCurriculumWorkflow(
        session_id=f"learning-curriculum-{learning_goal.lower().replace(' ', '-')}",
        debug_mode=True,
    )
    
    # Run the workflow
    curriculum_responses = workflow.run(learning_goal, use_cache=False)
    
    # Print the curriculum
    for response in curriculum_responses:
        if response.event == RunEvent.workflow_completed:
            workflow.print_curriculum(response.content)
            
            # Save the curriculum to a JSON file
            output_file = f"curriculum_{learning_goal.lower().replace(' ', '-')}.json"
            with open(output_file, "w") as f:
                json.dump(response.content, f, indent=2)
            
            print(f"\nCurriculum saved to {output_file}") 