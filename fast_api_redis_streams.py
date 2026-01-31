from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import redis.asyncio as redis
import asyncio

app = FastAPI()
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

@app.get("/stream-tokens/{request_id}")
async def stream_tokens(request_id: str):
    async def token_generator():
        stream_key = f"tokens:{request_id}"
        last_id = '0-0'
        
        while True:
            # Redis XREAD with BLOCK
            messages = await r.xread(
                {stream_key: last_id},
                count=1,
                block=5000  # Block for 5 seconds
            )
            
            if not messages:
                break
                
            for stream, entries in messages:
                for entry_id, data in entries:
                    token = data.get('token', '')
                    done = data.get('done', 'false')
                    
                    if done == 'true':
                        return
                    
                    # Yield to client
                    yield f"data: {token}\n\n"
                    last_id = entry_id
            
            await asyncio.sleep(0.01)
    
    return StreamingResponse(
        token_generator(),
        media_type="text/event-stream"
    )
    # HTTP connection stays open until generator completes