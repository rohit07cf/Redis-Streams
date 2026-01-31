#Producer Side (Streaming Tokens Out)

import redis
import time

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def stream_tokens(stream_name, tokens):
    """Stream tokens one by one to Redis"""
    for token in tokens:
        # Add each token to the stream
        entry_id = r.xadd(
            stream_name,
            {
                'token': token,
                'timestamp': time.time()
            }
        )
        print(f"Added token '{token}' with ID: {entry_id}")
        time.sleep(0.1)  # Simulate processing delay

# Example: Streaming LLM response tokens
tokens = ["Hello", " world", "!", " How", " can", " I", " help", " you", "?"]
stream_tokens('llm_response:123', tokens)