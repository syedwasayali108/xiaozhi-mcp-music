import os
import asyncio
import websockets
import yt_dlp
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Xiaozhi Universal Music")

@mcp.tool()
def search_and_stream_song(song_query: str) -> str:
    """Searches YouTube for any artist or song title and returns a direct audio stream URL."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1:'
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(song_query, download=False)
            if 'entries' in info and len(info['entries']) > 0:
                video_data = info['entries'][0]
            else:
                video_data = info
                
            stream_url = video_data['url']
            title = video_data.get('title', song_query)
            return f"Playing track '{title}': {stream_url}"
    except Exception as e:
        return f"Could not find song. Error: {str(e)}"

async def connect_to_xiaozhi():
    xiaozhi_ws_url = os.getenv("XIAOZHI_WSS_URL")
    if not xiaozhi_ws_url:
        print("Error: XIAOZHI_WSS_URL environment variable is missing!")
        return

    print("Connecting to Xiaozhi MCP Endpoint...")
    while True:
        try:
            async with websockets.connect(xiaozhi_ws_url) as ws:
                print("Successfully Connected to Xiaozhi Cloud!")
                while True:
                    msg = await ws.recv()
                    await ws.send("pong")
        except Exception as e:
            print(f"Connection lost: {e}. Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(connect_to_xiaozhi())

