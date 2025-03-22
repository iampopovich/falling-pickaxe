from googleapiclient.discovery import build
from config import config
from datetime import datetime
from pathlib import Path
from dateutil import parser
import os

# Initialize YouTube API client
youtube = build("youtube", "v3", developerKey=config["API_KEY"])

def get_live_streams(channel_id):
    """Retrieve all currently live streams for a given channel with their titles"""
    request = youtube.search().list(
        part="id,snippet",  # Include snippet to get titles
        channelId=channel_id,
        eventType="live",  # Only get currently live videos
        type="video"
    )
    response = request.execute()

    live_streams = []
    for item in response.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        live_streams.append({"video_id": video_id, "title": title})

    return live_streams

def get_live_stream(livestream_id):
    """Retrieve a single live stream by its ID"""
    request = youtube.videos().list(
        part="snippet",
        id=livestream_id
    )
    response = request.execute()

    if response.get("items"):
        return response["items"][0]
    else:
        return None

def get_live_chat_id(live_stream_id):
    response = youtube.videos().list(
        part="liveStreamingDetails",
        id=live_stream_id
    ).execute()
    
    return response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]

def get_live_chat_messages(live_chat_id):
    response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet,authorDetails"
    ).execute()
    
    for item in response["items"]:
        author = item["authorDetails"]["displayName"]
        message = item["snippet"]["displayMessage"]
        print(f"{author}: {message}")

# Store seen message IDs
seen_messages = set()
def get_new_live_chat_messages(live_chat_id):
    """Fetch and print only new chat messages that haven't been printed before."""
    response = youtube.liveChatMessages().list(
        liveChatId=live_chat_id,
        part="snippet,authorDetails"
    ).execute()

    # Define log directory
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists

    # Generate log file path
    log_file = log_dir / f"chat_{datetime.today().strftime('%Y-%m-%d')}.txt"

    for item in response["items"]:
        message_id = item["id"]  # Unique message ID
        if message_id not in seen_messages:
            seen_messages.add(message_id)  # Mark as seen
            
            author = item["authorDetails"]["displayName"]
            message = item["snippet"]["displayMessage"]
            timestamp = item["snippet"]["publishedAt"]  # UTC timestamp from API
            
            # Use dateutil to parse timestamp automatically
            timestamp = parser.parse(timestamp).strftime("%Y-%m-%d %H:%M:%S")

            # Write to file 
            with open(log_file, "a+", encoding="utf-8") as chat_file:
                chat_file.write(f"[{timestamp}] {author}: {message}\n")

            # Print with timestamp
            print(f"[{timestamp}] {author}: {message}")
    
    return response