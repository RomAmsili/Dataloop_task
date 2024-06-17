import httpx
import sys

BASE_URL_1 = 'http://localhost:8000'
BASE_URL_2 = 'http://localhost:8001'

async def send_request(url, endpoint, params=None):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{url}/{endpoint}", params=params)
        print(response.json())

async def main():
    command = sys.argv[1]
    param = int(sys.argv[2]) if len(sys.argv) > 2 else None

    if command == "start":
        if param is None:
            print("Error: start command requires pong_time_ms parameter")
            return
        await send_request(BASE_URL_1, "start", params={"pong_time": param})
        await send_request(BASE_URL_2, "start", params={"pong_time": param})
    elif command == "pause":
        await send_request(BASE_URL_1, "pause")
        await send_request(BASE_URL_2, "pause")
    elif command == "resume":
        await send_request(BASE_URL_1, "resume")
        await send_request(BASE_URL_2, "resume")
    elif command == "stop":
        await send_request(BASE_URL_1, "stop")
        await send_request(BASE_URL_2, "stop")
    else:
        print("Unknown command")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
