from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from prompts import Prompts
import re

class AI_Utilities:

    def initialize_llm(self,api_key):
        """Initialize Groq LLM with configured model"""

        self.llm =  ChatGroq(
            temperature=0,
            groq_api_key=api_key,
            model_name="llama-3.3-70b-versatile"
        )

    def __create_chain(self,llm, system_prompt, human_prompt):
        """Build Langchain prompt template for LLM evaluation"""
        template = ChatPromptTemplate([
            ("system", system_prompt),
            ("human", human_prompt),
        ])
        return template | llm | StrOutputParser()

    def evaluate(self, jd_content, cv_content,candiateMode):
        """Evaluate JD vs CV using parallel chain processing"""
       
        
        # Create parsing chains
        jd_chain = self.__create_chain(
            self.llm, Prompts.JD_PARSING_SYSTEM_PROMPT, Prompts.JD_PARSING_PROMPT
        )
        cv_chain = self.__create_chain(
            self.llm, Prompts.RESUME_PARSING_SYSTEM_PROMPT, Prompts.RESUME_PARSING_PROMPT
        )
        
        # Run parallel parsing
        parallel = RunnableParallel(
            jd_summary=jd_chain, 
            cv_summary=cv_chain
        )
        parsed_data = parallel.invoke({
            "jd_content": jd_content,
            "cv_content": cv_content
        })
        
        # Evaluate parsed data
        if candiateMode:
            evaluation_chain = self.__create_chain(
                    self.llm, Prompts.EVALUATION_SYSTEM_PROMPT_JSON, Prompts.EVALUATION_PROMPT_JSON)
            
            
                
            json_output =  evaluation_chain.invoke({
                "jd_summary": parsed_data["jd_summary"],
                "resume_summary": parsed_data["cv_summary"]
            })
            cleanJson =  self.__clean_json_string(json_output)
            try:
                import json
                evaluation = json.loads(cleanJson)
                evaluation['jd_summary'] = parsed_data["jd_summary"]
            except json.JSONDecodeError:
                
                evaluation = {}
                
            return evaluation
        else:
            evaluation_chain = self.__create_chain(
                    self.llm, Prompts.EVALUATION_SYSTEM_PROMPT, Prompts.EVALUATION_PROMPT)
            
            
                
            return evaluation_chain.invoke({
                "jd_summary": parsed_data["jd_summary"],
                "resume_summary": parsed_data["cv_summary"]
            })
            
    def generate_suggestions(self,gaps):
        """Generate actionable CV improvement suggestions"""
        
        suggestions_chain = self.__create_chain(
            self.llm,
            Prompts.SUGGESTIONS_SYSTEM_PROMPT,
            Prompts.SUGGESTIONS_HUMAN_PROMPT
        )
        
        return suggestions_chain.invoke({"gaps": gaps})

    def rewrite_cv(self, cv_content, suggestions, job_requirements):
       
        cv_chain = self.__create_chain(
            self.llm,
            Prompts.CV_REWRITE_SYSTEM_PROMPT,
            Prompts.CV_REWRITE_HUMAN_PROMPT
        )
        
        return cv_chain.invoke({
            "original_cv": cv_content,
            "suggestions": suggestions,
            "job_requirements": job_requirements
        })
        

    def json_to_markdown_report(self,json_eval):
        # Build the positives section
        # positives = json_eval.get("positives", [])
        # positives_block = (
        #     "- " + "\n- ".join(positives) if positives else
        #     "- No matches found"
        # )
        
        # Build the gaps section
        gaps = json_eval.get("gaps", [])
        gaps_block = (
            "- " + "\n- ".join(gaps) if gaps else
            "- No gaps detected"
        )
        
        return f"""
    **Job Title:** {json_eval.get("job_title", "N/A")}  
    **Overall Match Score:** {json_eval.get("overall_score", "N/A")} 
     
**Gaps:**
{gaps_block}
    """

    def __clean_json_string(self,json_string):
        pattern = r'^```json\s*(.*?)\s*```$'
        cleaned_string = re.sub(pattern, r'\1', json_string, flags=re.DOTALL)
        return cleaned_string.strip()