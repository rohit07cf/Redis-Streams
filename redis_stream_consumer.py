#Consumer Side (Streaming Tokens Out)

import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

def consume_tokens(stream_name):
    """Read tokens from stream in real-time"""
    # Start from the beginning or use '0-0'
    # For real-time: use '$' to only get new messages
    last_id = '0-0'
    
    while True:
        # XREAD with BLOCK waits for new entries
        messages = r.xread(
            {stream_name: last_id},
            count=1,
            block=1000  # Block for 1 second
        )
        
        if messages:
            for stream, entries in messages:
                for entry_id, data in entries:
                    print(f"Received: {data['token']}")
                    last_id = entry_id
        else:
            # No new messages, could break or continue
            print("No new messages...")
            break

# Read the stream
consume_tokens('llm_response:123')