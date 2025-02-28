import json
from openai import OpenAI
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_embedding(text):
    """Get embedding for a single text using text-embedding-3-small"""
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text,
            encoding_format="float"
        )
        # Small delay to respect rate limits
        time.sleep(0.5)
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embedding: {e}")
        return None

def main():
    # Load the candidate summaries
    with open('candidate_summaries.json', 'r', encoding='utf-8') as f:
        candidates = json.load(f)
    
    # Process first 5 candidates
    for i, candidate in enumerate(candidates[:5]):
        print(f"\nProcessing candidate {i+1}: {candidate['name']}")
        
        # Get embedding for RAG text
        embedding = get_embedding(candidate['rag_text'])
        
        if embedding:
            # Print first 5 and last 5 dimensions of the embedding vector
            print(f"Embedding vector (showing first 5 and last 5 dimensions of {len(embedding)} total):")
            print("First 5:", embedding[:5])
            print("Last 5:", embedding[-5:])

if __name__ == "__main__":
    main() 