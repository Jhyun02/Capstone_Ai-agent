"""
ELI5 Tutor Streamlit Application

This module implements a Streamlit-based user interface for the ELI5 Tutor application.
It provides a clean, modern interface for interacting with the ELI5 agent and viewing
cache statistics.

Features:
    - Interactive chat interface
    - Cache statistics visualization
    - Response metadata display
    - Clean, modern UI with custom styling
"""

import streamlit as st
from agents.eli5_agent import ELI5Agent
from datetime import datetime
import json
import pandas as pd
from cache.prompt_cache import clear_cache

# Page configuration for Streamlit
st.set_page_config(
    page_title="ELI5 Tutor",
    page_icon="📚",
    layout="wide"
)

# Initialize session state for persistent data
if 'agent' not in st.session_state:
    st.session_state.agent = ELI5Agent()
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def format_timestamp(timestamp: str) -> str:
    """
    Format an ISO timestamp into a human-readable string.
    
    Args:
        timestamp (str): ISO format timestamp string
        
    Returns:
        str: Formatted timestamp string (YYYY-MM-DD HH:MM:SS)
    """
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def display_cache_stats():
    """
    Display cache statistics with a clean UI.
    
    This function shows:
    - Total number of cached entries
    - Total cache size
    - Oldest and newest entry timestamps
    All statistics are displayed in a clean, card-like format.
    """
    stats = st.session_state.agent.get_cache_info()
    
    # Custom CSS for styling the statistics display
    st.markdown("""
        <style>
        .stats-container {
            background-color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            border: none;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stats-title {
            font-size: 1rem;
            color: #31333F;
            margin-bottom: 0.5rem;
        }
        
        .stats-value {
            font-size: 0.9rem;
            color: #666666;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display statistics in a clean container
    st.markdown('<div class="stats-container">', unsafe_allow_html=True)
    st.markdown('<div class="stats-title">📊 Cache Statistics</div>', unsafe_allow_html=True)
    
    # Split statistics into two columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f'<div class="stats-value">Total Entries: {stats["total_entries"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stats-value">Total Size: {stats["total_size_bytes"] / 1024:.1f} KB</div>', unsafe_allow_html=True)
    
    with col2:
        if stats['oldest_entry']:
            st.markdown(f'<div class="stats-value">Oldest: {format_timestamp(stats["oldest_entry"])}</div>', unsafe_allow_html=True)
        if stats['newest_entry']:
            st.markdown(f'<div class="stats-value">Newest: {format_timestamp(stats["newest_entry"])}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def main():
    """
    Main application function.
    
    This function:
    1. Sets up the sidebar with controls
    2. Creates the main chat interface
    3. Handles user input and responses
    4. Displays chat history with metadata
    """
    # Sidebar setup
    with st.sidebar:
        st.title("📚 ELI5 Tutor")
        st.markdown("""
        Ask any question and get a simple, easy-to-understand explanation!
        
        ### Features
        - 🤖 AI-powered explanations
        - 💾 Response caching
        - 🔍 Semantic search
        - 📊 Cache statistics
        """)
        
        # Control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        with col2:
            if st.button("🗑️ Clear Cache"):
                clear_cache()
                st.success("Cache cleared!")
                st.rerun()
            
        if st.button("📊 Show Cache Stats"):
            display_cache_stats()

    # Main content area
    st.title("Ask Your Question")
    
    # Chat input form
    with st.form("question_form", clear_on_submit=True):
        user_input = st.text_input("What would you like to understand?", key="user_input")
        submitted = st.form_submit_button("Ask")
        
        if submitted and user_input:
            # Get response from agent
            response, metadata = st.session_state.agent.explain(user_input)
            
            # Add to chat history
            st.session_state.chat_history.append({
                "question": user_input,
                "response": response,
                "metadata": metadata
            })
            
            # Rerun to update the display
            st.rerun()
        
    # Display chat history
    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        with st.container():
            # Chat card with question and response
            st.markdown('<div class="chat-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="question">🧑 {chat["question"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="response">🤖 {chat["response"]}</div>', unsafe_allow_html=True)
            
            # Display metadata using Streamlit's native components
            if chat['metadata'].get('cached', False):
                st.info(f"💾 From cache ({format_timestamp(chat['metadata']['timestamp'])})")
            else:
                st.success(f"🤖 Generated with {chat['metadata']['model']} (temp: {chat['metadata']['temperature']})")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 