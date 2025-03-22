from googleapiclient.discovery import build
from config import config

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