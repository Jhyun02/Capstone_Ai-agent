from agno.agent import Agent, RunResponse
import json
from instructions import Instructions
from utils import getModel

MESSAGE_SUFFIX = "\n-If any of these prametrs are missing please create a response for the user to provide them in a conversational manner and add return this response in the message key"

class TripConversationAgent(Agent):
    
    
    def __init__(self, api_key,llm_mode:str):
        
        super().__init__(
            name="Conversational Trip Data Extractor",
            description="Have a conversation with the user about their trip to extract their trip requirements in a structured format.",
            model=getModel(llm_mode,api_key),
          
           # - Make sure to always add a message key to the output JSON.
           #  - The retuned JSON should only have the follwing keys trip_type, origin, destination, dates,accommodation, travelers,budget,requirements, message. No extra keys should be added and None should be assigned to keys if they do not have a value
            instructions=Instructions.CONVERSATION_INSTRUCTIONS,
           
            add_datetime_to_instructions = True
            
        )
        self.finalParams = {
            "trip_type": None,
            "origin": None,
            "destination": None,
            "dates": None,
            "travelers": None,
            "accommodation": None,
            "budget": None,
            "requirements": None
            
            
        }
        self.final_param_keys = self.finalParams.keys()
        self.suffix = ""
        

    
    def __process_tripdata(self,params_llm):
        
       
        missing = []
        
        params_llm_keys = params_llm.keys()
        for key in self.final_param_keys:
            try:
                
                if not self.finalParams[key]:
                    if key in params_llm_keys:
                        if params_llm[key]:
                            self.finalParams[key] = params_llm[key]
                        else:
                            missing.append(key)
                    else:
                        missing.append(key)
                    
            except:
                pass
       
            
        if missing:
            missing_params = ", ".join(missing)
            return {"user_message":f"Please provide the follwing missing params which are required  : {missing_params}.",
                    "query_suffix":f"\n -Identify the following parameters only {missing_params} and retunr only these parameters in the output JSON.{MESSAGE_SUFFIX}","missing":True}
        else:
            return {"user_message":"Thank you! Planning your trip..",
                    "query_suffix":"",
                    "missing":False}
       
       
            
            
    def reset(self):
        self.finalParams = {
            "trip_type": None,
            "origin": None,
            "destination": None,
            "dates": None,
            "travelers": None,
            "accommodation": None,
            "budget": None,
            "requirements": None
            
            
        }
       
        self.suffix = ""

        

    def process_query(self, query):
        
       
        if len(self.suffix) == 0:
            
            keys = ", ".join(self.final_param_keys)
            final_query = query+f"\n-Identify the following parameters only {keys} and return only these keys in the output JSON.{MESSAGE_SUFFIX}"
        else:
            final_query = query+"\n-"+self.suffix
        
        try:
            
            response: RunResponse = self.run(final_query)
            
            """Only in case of deepseek"""
            cleaned  = response.content.split("</think>")
            if len(cleaned) > 1:
                modified = cleaned[1].replace("```json", "")
            else:
                modified = cleaned[0].replace("```json", "")
            modified = modified.replace("```", "")
            
            params = json.loads(modified)
            
            result = self.__process_tripdata(params)
            self.suffix = result["query_suffix"]
            user_message = result["user_message"]
            have_further_conversation = result["missing"]
      
            if not params["message"] or not have_further_conversation:
                return {"message":user_message,"have_further_conversation":have_further_conversation,'data':self.finalParams}
                
            else:
                return {"message":params["message"],"have_further_conversation":have_further_conversation,'data':self.finalParams}
        except:
                return {"message":"There was a problem 😖 please try again.","have_further_conversation":True,'data':self.finalParams}