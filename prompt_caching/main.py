from agents.eli5_agent import ELI5Agent
from datetime import datetime
import json

def format_timestamp(timestamp: str) -> str:
    """Format timestamp for display."""
    dt = datetime.fromisoformat(timestamp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def display_cache_stats(agent: ELI5Agent):
    """Display cache statistics."""
    stats = agent.get_cache_info()
    print("\n📊 Cache Statistics:")
    print(f"Total entries: {stats['total_entries']}")
    print(f"Total size: {stats['total_size_bytes'] / 1024:.2f} KB")
    if stats['oldest_entry']:
        print(f"Oldest entry: {format_timestamp(stats['oldest_entry'])}")
    if stats['newest_entry']:
        print(f"Newest entry: {format_timestamp(stats['newest_entry'])}")

def main():
    agent = ELI5Agent()
    
    print("\n📚 Welcome to ELI5 Tutor!")
    print("Type your concept or question (or 'exit' to quit, 'stats' for cache statistics)\n")
    
    while True:
        question = input("🧑 Ask: ").strip()
        
        if question.lower() == "exit":
            break
        elif question.lower() == "stats":
            display_cache_stats(agent)
            continue
            
        response, metadata = agent.explain(question)
        
        print("\n🤖 ELI5 Response:")
        print(response)
        
        # Display metadata
        print("\nℹ️ Response Info:")
        print(f"Source: {'Cache' if metadata['cached'] else 'LLM'}")
        if metadata['cached']:
            print(f"Cached at: {format_timestamp(metadata['timestamp'])}")
        else:
            print(f"Model: {metadata['model']}")
            print(f"Temperature: {metadata['temperature']}")
            print(f"Generated at: {format_timestamp(metadata['timestamp'])}")
        print()

if __name__ == "__main__":
    main()
