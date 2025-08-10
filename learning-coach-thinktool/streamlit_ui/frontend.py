#!/usr/bin/env python3
"""
Streamlit UI for the Learning Curriculum Generator.
Provides an interface for users to input their learning goals and view the generated curriculum.
"""

import streamlit as st
import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import the workflow
sys.path.append(str(Path(__file__).parent.parent))

from agents.learning_curriculum_workflow import LearningCurriculumWorkflow
from agno.utils.log import logger

# Set page config
st.set_page_config(
    page_title="Learning Curriculum Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom CSS
st.markdown("""
<style>
    /* Global styles */
    .main {
        background-color: #121212;
        color: #e0e0e0;
    }
    
    /* Card styles */
    .stExpander {
        border: none !important;
        border-radius: 10px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
        background-color: #1e1e1e !important;
        overflow: hidden !important;
    }
    
    .stExpander > details {
        border: none !important;
    }
    
    .stExpander > details > summary {
        background-color: #2a2a2a !important;
        padding: 15px 20px !important;
        border-radius: 10px 10px 0 0 !important;
        font-weight: bold !important;
        color: #4dabf7 !important;
        border-bottom: 1px solid #333 !important;
    }
    
    .stExpander > details > summary:hover {
        background-color: #333 !important;
    }
    
    .stExpander > details > div {
        padding: 20px !important;
        background-color: #1e1e1e !important;
    }
    
    /* Section headers */
    .section-header {
        font-size: 1.3em !important;
        font-weight: bold !important;
        color: #4dabf7 !important;
        margin-top: 15px !important;
        margin-bottom: 10px !important;
        padding-bottom: 8px !important;
        border-bottom: 2px solid #333 !important;
    }
    
    /* Resource styles */
    .resource-item {
        background-color: #2a2a2a !important;
        padding: 15px !important;
        border-radius: 8px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
        transition: transform 0.2s ease !important;
    }
    
    .resource-item:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3) !important;
    }
    
    .free-resource {
        border-left: 4px solid #4caf50 !important;
    }
    
    .paid-resource {
        border-left: 4px solid #f39c12 !important;
    }
    
    .resource-title {
        font-size: 1.1em !important;
        font-weight: bold !important;
        color: #4dabf7 !important;
        margin-bottom: 5px !important;
    }
    
    .resource-type {
        font-size: 0.9em !important;
        color: #aaa !important;
        margin-bottom: 8px !important;
    }
    
    .resource-description {
        margin-bottom: 10px !important;
        line-height: 1.5 !important;
        color: #e0e0e0 !important;
    }
    
    .resource-meta {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 8px !important;
        margin-top: 10px !important;
        font-size: 0.85em !important;
        color: #aaa !important;
    }
    
    .resource-difficulty {
        display: inline-block !important;
        padding: 3px 8px !important;
        border-radius: 4px !important;
        font-size: 0.8em !important;
        font-weight: bold !important;
    }
    
    .difficulty-beginner {
        background-color: #1b5e20 !important;
        color: #a5d6a7 !important;
    }
    
    .difficulty-intermediate {
        background-color: #e65100 !important;
        color: #ffe0b2 !important;
    }
    
    .difficulty-advanced {
        background-color: #b71c1c !important;
        color: #ffcdd2 !important;
    }
    
    .resource-link {
        display: inline-block !important;
        margin-top: 10px !important;
        color: #4dabf7 !important;
        text-decoration: none !important;
        font-weight: bold !important;
    }
    
    .resource-link:hover {
        text-decoration: underline !important;
    }
    
    /* Progress bar styles */
    .progress-container {
        width: 100% !important;
        background-color: #333 !important;
        border-radius: 10px !important;
        margin-bottom: 25px !important;
        overflow: hidden !important;
    }
    
    .progress-bar {
        height: 25px !important;
        background: linear-gradient(90deg, #4dabf7, #4caf50) !important;
        border-radius: 10px !important;
        text-align: center !important;
        line-height: 25px !important;
        color: white !important;
        font-weight: bold !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.3) !important;
    }
    
    /* Topic and concept styles */
    .topic-item, .concept-item {
        background-color: #2a2a2a !important;
        padding: 10px 15px !important;
        border-radius: 6px !important;
        margin-bottom: 8px !important;
        border-left: 3px solid #4dabf7 !important;
        color: #e0e0e0 !important;
    }
    
    .project-item {
        background-color: #2a2a2a !important;
        padding: 15px !important;
        border-radius: 8px !important;
        margin-bottom: 15px !important;
        border-left: 4px solid #f39c12 !important;
    }
    
    .project-title {
        font-weight: bold !important;
        color: #f39c12 !important;
        margin-bottom: 8px !important;
    }
    
    /* Button styles */
    .stButton > button {
        background-color: #4dabf7 !important;
        color: white !important;
        border-radius: 5px !important;
        padding: 10px 20px !important;
        font-weight: bold !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button:hover {
        background-color: #339af0 !important;
    }
    
    /* Tab styles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 5px 5px 0 0 !important;
        padding: 10px 20px !important;
        background-color: #2a2a2a !important;
        color: #aaa !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #4dabf7 !important;
        color: white !important;
    }
    
    /* Text area and input styles */
    .stTextArea > div > div > textarea {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border: 1px solid #333 !important;
    }
    
    /* JSON viewer styles */
    .stJson {
        background-color: #2a2a2a !important;
        border-radius: 8px !important;
        padding: 15px !important;
        color: #e0e0e0 !important;
    }
    
    /* Footer styles */
    .footer {
        color: #aaa !important;
        text-align: center !important;
        margin-top: 30px !important;
        padding: 20px !important;
        border-top: 1px solid #333 !important;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.title("Learning Curriculum Generator")
st.markdown("""
This tool generates a personalized learning curriculum based on your learning goals.
Enter your goal below and click 'Generate Curriculum' to get started.
""")

# Input section
with st.container():
    learning_goal = st.text_area(
        "What do you want to learn?",
        placeholder="e.g., Learn Flutter app development from beginner to advanced",
        height=100,
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_button = st.button("Generate Curriculum", type="primary", use_container_width=True)

# Initialize session state for curriculum
if 'curriculum' not in st.session_state:
    st.session_state.curriculum = None
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

# Function to generate curriculum
def generate_curriculum(goal):
    """Generate curriculum using the workflow."""
    # Initialize the workflow
    workflow = LearningCurriculumWorkflow(
        session_id=f"learning-curriculum-{goal.lower().replace(' ', '-')}",
        debug_mode=True,
    )
    
    # Run the workflow
    response = workflow.run_workflow(learning_goal=goal)
    logger.info(f"Curriculum response: {response}")
    
    # Check if the response is valid and contains curriculum data
    if response and hasattr(response, 'content') and response.content:
        return response.content
    
    return None

# Handle generation button click
if generate_button and learning_goal and not st.session_state.is_generating:
    st.session_state.is_generating = True
    with st.spinner("Generating your personalized curriculum... This may take a few minutes."):
        st.session_state.curriculum = generate_curriculum(learning_goal)
    st.session_state.is_generating = False

# Display curriculum if available
if st.session_state.curriculum:
    st.markdown("## Your Personalized Learning Curriculum")
    
    # Progress bar at the top
    total_weeks = len(st.session_state.curriculum["curriculum"])
    progress_percent = 100 / total_weeks
    
    st.html(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: 100%;">{total_weeks}-Week Learning Journey</div>
    </div>
    """)
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Weekly Cards", "Complete Curriculum"])
    
    with tab1:
        # Display each week in an expandable card
        for week in st.session_state.curriculum["curriculum"]:
            week_num = week["week"]
            topics = ", ".join(week["topics"])
            
            with st.expander(f"Week {week_num}: {topics}", expanded=False):
                # Topics
                st.markdown("### Topics")
                for topic in week["topics"]:
                    st.html(f"""
                    <div class="topic-item">
                        {topic}
                    </div>
                    """)
                
                # Key Concepts
                st.markdown("### Key Concepts")
                for concept in week["concepts"]:
                    st.html(f"""
                    <div class="concept-item">
                        {concept}
                    </div>
                    """)
                
                # Project if available
                if week.get("project"):
                    st.markdown("### Mini Project")
                    st.html(f"""
                    <div class="project-item">
                        <div class="project-title">Project Description:</div>
                        {week["project"]}
                    </div>
                    """)
                
                # Resources
                if "resources" in st.session_state.curriculum and str(week_num) in st.session_state.curriculum["resources"]:
                    week_resources = st.session_state.curriculum["resources"][str(week_num)]["resources"]
                    
                    if week_resources:
                        st.markdown("### Learning Resources")
                        
                        # Categorize resources as free/paid
                        free_resources = [r for r in week_resources if r.get("cost", "").lower() == "free"]
                        paid_resources = [r for r in week_resources if r not in free_resources]
                        
                        if free_resources:
                            st.markdown("#### Free Resources")
                            for resource in free_resources:
                                # Determine difficulty class
                                difficulty_class = "difficulty-beginner"
                                if resource.get("difficulty") == "intermediate":
                                    difficulty_class = "difficulty-intermediate"
                                elif resource.get("difficulty") == "advanced":
                                    difficulty_class = "difficulty-advanced"
                                
                                st.html(f"""
                                <div class="resource-item free-resource">
                                    <div class="resource-title">{resource['title']}</div>
                                    <div class="resource-type">Type: {resource['type']}</div>
                                    <div class="resource-description">{resource['description']}</div>
                                    <div class="resource-meta">
                                        <span class="resource-difficulty {difficulty_class}">{resource.get('difficulty', 'beginner').capitalize()}</span>
                                        <span>⏱️ {resource.get('estimated_time', 'N/A')}</span>
                                        <span>📝 {resource.get('format', 'N/A').capitalize()}</span>
                                    </div>
                                    <a href="{resource['url']}" target="_blank" class="resource-link">Access Resource</a>
                                </div>
                                """)
                        
                        if paid_resources:
                            st.markdown("#### Paid Resources")
                            for resource in paid_resources:
                                # Determine difficulty class
                                difficulty_class = "difficulty-beginner"
                                if resource.get("difficulty") == "intermediate":
                                    difficulty_class = "difficulty-intermediate"
                                elif resource.get("difficulty") == "advanced":
                                    difficulty_class = "difficulty-advanced"
                                
                                st.html(f"""
                                <div class="resource-item paid-resource">
                                    <div class="resource-title">{resource['title']}</div>
                                    <div class="resource-type">Type: {resource['type']}</div>
                                    <div class="resource-description">{resource['description']}</div>
                                    <div class="resource-meta">
                                        <span class="resource-difficulty {difficulty_class}">{resource.get('difficulty', 'beginner').capitalize()}</span>
                                        <span>⏱️ {resource.get('estimated_time', 'N/A')}</span>
                                        <span>📝 {resource.get('format', 'N/A').capitalize()}</span>
                                    </div>
                                    <a href="{resource['url']}" target="_blank" class="resource-link">Access Resource</a>
                                </div>
                                """)
                
                # Assessments

    
    with tab2:
        # Display the complete curriculum as JSON
        st.json(st.session_state.curriculum)
    
    # Download button for JSON
    st.download_button(
        label="Download Curriculum as JSON",
        data=json.dumps(st.session_state.curriculum, indent=2),
        file_name=f"curriculum_{learning_goal.lower().replace(' ', '-')}.json",
        mime="application/json",
    )

# Add footer
st.markdown("---")
st.html("""
<div class="footer">
    <p>Powered by AI • Learning Curriculum Generator</p>
</div>
""")
