import os
import json
import hashlib
from datetime import datetime
from typing import Optional, Dict, Any
import numpy as np
from sentence_transformers import SentenceTransformer

CACHE_DIR = "./cache/data"
SIMILARITY_THRESHOLD = 0.85  # Adjust this threshold as needed
os.makedirs(CACHE_DIR, exist_ok=True)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def _hash_key(prompt: str) -> str:
    """Generate a hash key for the prompt."""
    return hashlib.md5(prompt.strip().lower().encode()).hexdigest()

def _compute_embedding(text: str) -> np.ndarray:
    """Compute embedding for the given text."""
    return model.encode(text)

def _compute_similarity(embedding1: np.ndarray, embedding2: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings."""
    return float(np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2)))

def load_response(prompt: str, use_semantic_search: bool = True) -> Optional[Dict[str, Any]]:
    """
    Load response from cache, optionally using semantic search.
    
    Args:
        prompt: The input prompt
        use_semantic_search: Whether to use semantic search for finding similar prompts
        
    Returns:
        Dictionary containing response and metadata if found, None otherwise
    """
    # First try exact match
    key = _hash_key(prompt)
    path = os.path.join(CACHE_DIR, f"{key}.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)

    if not use_semantic_search:
        return None

    # Try semantic search
    prompt_embedding = _compute_embedding(prompt)
    best_match = None
    best_similarity = 0

    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith('.json'):
            continue
            
        with open(os.path.join(CACHE_DIR, filename)) as f:
            cached_data = json.load(f)
            cached_embedding = _compute_embedding(cached_data['prompt'])
            similarity = _compute_similarity(prompt_embedding, cached_embedding)
            
            if similarity > best_similarity and similarity >= SIMILARITY_THRESHOLD:
                best_similarity = similarity
                best_match = cached_data

    return best_match

def save_response(prompt: str, response: str, metadata: Optional[Dict[str, Any]] = None) -> None:
    """
    Save response to cache with metadata.
    
    Args:
        prompt: The input prompt
        response: The response to cache
        metadata: Optional metadata about the response
    """
    key = _hash_key(prompt)
    cache_data = {
        "prompt": prompt,
        "response": response,
        "embedding": _compute_embedding(prompt).tolist(),
        "timestamp": datetime.now().isoformat(),
        "metadata": metadata or {}
    }
    
    with open(os.path.join(CACHE_DIR, f"{key}.json"), "w") as f:
        print(f"🔁 Saving response to cache: {prompt[:50]}...")
        json.dump(cache_data, f)

def clear_cache() -> None:
    """Clear all cached responses."""
    for filename in os.listdir(CACHE_DIR):
        if filename.endswith('.json'):
            os.remove(os.path.join(CACHE_DIR, filename))

def get_cache_stats() -> Dict[str, Any]:
    """Get statistics about the cache."""
    stats = {
        "total_entries": 0,
        "total_size_bytes": 0,
        "oldest_entry": None,
        "newest_entry": None
    }
    
    for filename in os.listdir(CACHE_DIR):
        if not filename.endswith('.json'):
            continue
            
        path = os.path.join(CACHE_DIR, filename)
        stats["total_entries"] += 1
        stats["total_size_bytes"] += os.path.getsize(path)
        
        with open(path) as f:
            data = json.load(f)
            timestamp = datetime.fromisoformat(data["timestamp"])
            
            if stats["oldest_entry"] is None or timestamp < datetime.fromisoformat(stats["oldest_entry"]):
                stats["oldest_entry"] = data["timestamp"]
            if stats["newest_entry"] is None or timestamp > datetime.fromisoformat(stats["newest_entry"]):
                stats["newest_entry"] = data["timestamp"]
    
    return stats
