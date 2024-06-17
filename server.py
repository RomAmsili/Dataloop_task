from fastapi import FastAPI, HTTPException
import httpx
import asyncio
import os

app = FastAPI()

pong_time_ms = 1000
is_paused = False
is_stopped = False
opponent_url = os.getenv('OPPONENT_URL', 'http://localhost:8001')
ping_task = None

@app.get("/ping")
async def ping():
    global ping_task
    print('Received ping')
    if not is_paused and not is_stopped:
        await asyncio.sleep(pong_time_ms / 1000)
        ping_task = asyncio.create_task(send_ping())
    return {"message": "pong"}

async def send_ping():
    try:
        print(f'Sending ping to {opponent_url}/ping')
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{opponent_url}/ping")
            print(f'Received response: {response.text}')
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {exc.request.url!r}: {exc}")
    except Exception as exc:
        print(f"An unexpected error occurred: {exc}")

@app.post("/start")
async def start(pong_time: int):
    global pong_time_ms, is_paused, ping_task, is_stopped
    pong_time_ms = pong_time
    is_paused = False
    is_stopped = False
    if ping_task:
        ping_task.cancel()
    ping_task = asyncio.create_task(send_ping())
    return {"message": "Game started"}

@app.post("/pause")
async def pause():
    global is_paused, ping_task
    is_paused = True
    if ping_task:
        ping_task.cancel()
    return {"message": "Game paused"}

@app.post("/resume")
async def resume():
    global is_paused, ping_task, is_stopped
    if is_stopped:
        return {"message": "Game stopped. start a new game"}
    is_paused = False
    if ping_task:
        ping_task.cancel()
    ping_task = asyncio.create_task(send_ping())
    return {"message": "Game resumed"}

@app.post("/stop")
async def stop():
    global ping_task, is_stopped
    is_stopped = True
    if ping_task:
        ping_task.cancel()
    return {"message": "Game stopped"}
