import streamlit as st
from conversation import TripConversationAgent
from travel_itenary_workflow import ItenaryGeneratorWorkflow


st.set_page_config(
    page_title="AI Travel Planner", 
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/vivekpathania/ai-experiments/issues"
    }
    )


st.title("AI Travel Planner")
if "are_keys_avaibale" not in st.session_state:
    st.session_state["are_keys_avaibale"] = False 
        


with st.sidebar:
    
    llm_mode = st.radio("Select Model Provider", ["Groq", "OpenAI"], horizontal = True)
    
    api_key_llm = st.text_input(
        "Groq or OpenAI API Key", key="api_key_llm", type="password"
        
        
    )
    st.html(
    '<a href="https://console.groq.com/keys">Get your API key from Groq Platform</a>'
    )
    st.html(
    '<a href="https://console.groq.com/keys">Get your API key from OpenAI</a>'
    )
    
    st.divider()
    web_search_mode = st.radio("Select Web Search Tool", ["Tavily", "SerpApi"], horizontal = True)
    
    api_key_search_tool = st.text_input(
        "Travily Or SerpApi Key", key="api_key_search_tool", type="password"
        
    )
    
    st.html(
    '<a href="https://app.tavily.com">Get your API key from Tavily</a>'
    )
    st.html(
    '<a href="https://serpapi.com/">Get your API key from SerpApi</a>'
    )
   
    
    if st.button("Set keys"):
        
        #if "conversation_agent" not in st.session_state:
        
        st.session_state["conversation_agent"] = TripConversationAgent(api_key=api_key_llm,llm_mode=llm_mode) 
                
        #if "itenaryGeneratorWorkflow" not in st.session_state:
        st.session_state["itenaryGeneratorWorkflow"] = ItenaryGeneratorWorkflow(api_key_llm=api_key_llm,api_key_search_tool=api_key_search_tool,search_tool=web_search_mode,llm_mode=llm_mode)
            
        st.session_state["are_keys_avaibale"] = True
        
    if not st.session_state["are_keys_avaibale"]:
        st.warning("Please enter both keys to get started.")
    else:
        st.success("API keys are avaibale.")
        
    st.divider()
    if st.button("Clear Conversation"):
        st.session_state.messages.clear() 
        if "conversation_agent" in st.session_state:
            st.session_state["conversation_agent"].reset()
            
        
    


# Main App Logic
# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_state" not in st.session_state:
    st.session_state.conversation_state = {}

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
user_query = st.chat_input("Start by describing your trip (e.g., 'Family holiday from London to Paris for 4 days with 3 adults and 1 child')")


if user_query:
    # Append user message
    if st.session_state["are_keys_avaibale"]:
        
    
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)
        
        response =  st.session_state['conversation_agent'].process_query(user_query)
        

        # Append assistant response
        if response['have_further_conversation']:
            st.session_state.messages.append({"role": "assistant", "content": response["message"]})
            with st.chat_message("assistant"):
                st.markdown(response["message"])
        else:
            with st.chat_message("assistant"):
                st.markdown(response["message"])
        
            with st.spinner("Planning your trip... 🌍\n\n1️⃣ Fetching flight options\n2️⃣ Searching hotels\n3️⃣ Compiling activities"):
                itenary_markdown = st.session_state["itenaryGeneratorWorkflow"].run(response['data'])
            with st.chat_message("assistant"):
                st.markdown(itenary_markdown.content)
                st.download_button(
                        label="Download Itinerary",
                        data=itenary_markdown.content,
                        file_name="itinerary.md",
                        mime="text/markdown"
                    )
    else:
        st.toast('Please enter both keys to get started.', icon='⚠️')
        

    
    
            

                



                    

