from agno.agent import Agent, RunResponse
from agno.utils.log import logger
from agno.workflow import Workflow
from instructions import Instructions
from utils import getModel,getSearchTool

class ItenaryGeneratorWorkflow(Workflow):
    description: str = "Comprehensive Travel Itinerary Workflow"
    def __init__(self, api_key_llm:str,api_key_search_tool:str,search_tool:str,llm_mode:str):
        
        self.travel_query_generator: Agent = Agent(
            name="Travel Query Enhancer",
            description="Generates structured trip-specific queries",
            instructions= Instructions.QUERY_ENHANCER_INSTRUCTIONS,
            model=getModel(llm_mode,api_key_llm),
            debug_mode=False,
            
            add_datetime_to_instructions = True
        )
        

        self.researcher = Agent(
            name="Travel Data Gatherer",
            description="Collects real-time travel data and local information",
            instructions=Instructions.RESEARCH_INSTRUCTIONS,
            tools=[getSearchTool(search_tool=search_tool,api_key_search_tool=api_key_search_tool)],
            model=getModel(llm_mode,api_key_llm),
            debug_mode=False,
           
            add_datetime_to_instructions = True
        )

        self.travel_agent = Agent(
            name="Itinerary Compiler",
            description="Generates visually appealing markdown itinerary",
            instructions=Instructions.ITINERARY_INSTRUCTIONS,
            model=getModel(llm_mode,api_key_llm),
            markdown=True,
            debug_mode=False,
                
            add_datetime_to_instructions = True
        )
        
    def __generate_trip_query(self,queryJSON):                                                                                                                                                                                                                                                                                                 
            
        query = f"""I want to plan a {queryJSON['trip_type']} trip from {queryJSON['origin']} to {queryJSON['destination']} 
                      from {queryJSON['dates']['start_date']} to {queryJSON['dates']['end_date']} 
                      for {queryJSON['travelers']} travelers. Budget: {queryJSON['budget']}.
                      Needs: {queryJSON['requirements']}.
                      Budget: {queryJSON['budget']}.
                      Please include multiple options for flights, accomodation, and transportation."""                                                                                                                                                                                                                                                                                         
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
        return query   
    
    
               

    def run(self, payload: str) -> RunResponse:
        
        raw_query = self.__generate_trip_query(payload)
        
        # Step 1: Generate enhanced query
        enhanced_query = self.travel_query_generator.run(raw_query)
        #logger.info(f"Enhanced Query: {enhanced_query.content}")

        # Step 2: Collect travel data
        data = self.researcher.run(enhanced_query.content)
        #logger.info(f"Collected Data: {data.content}")

        # # Step 3: Generate itinerary
        itinerary = self.travel_agent.run(data.content)
        return itinerary

