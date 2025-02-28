import json
from openai import OpenAI
import time
from dotenv import load_dotenv
import os
from pinecone import Pinecone

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Initialize Pinecone
pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))
index = pc.Index("mercor")

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
    
    # Start from candidate 970
    start_index = 970
    remaining_candidates = candidates[start_index:]
    
    print(f"\nProcessing {len(remaining_candidates)} candidates starting from index {start_index}")
    
    for i, candidate in enumerate(remaining_candidates, start=start_index):
        print(f"Processing candidate {i+1}: {candidate['name']}")
        
        # Get embedding for RAG text
        embedding = get_embedding(candidate['rag_text'])
        
        if embedding:
            # Create vector object with id, values, and metadata
            vector = {
                "id": f"candidate_{i}",  # Keep original indexing for consistency
                "values": embedding,
                "metadata": {
                    "name": candidate['name'],
                    "email": candidate['email'],
                    "rag_text": candidate['rag_text']
                }
            }
            
            try:
                # Upload single vector to Pinecone
                index.upsert(vectors=[vector])
                print(f"Successfully uploaded vector for {candidate['name']}")
            except Exception as e:
                print(f"Error uploading to Pinecone for {candidate['name']}: {e}")
        else:
            print(f"Failed to get embedding for {candidate['name']}")

if __name__ == "__main__":
    main() 