from youtube import get_live_streams, get_live_stream, get_new_live_chat_messages, get_live_chat_id
from config import config 
import time

print("Fetching live streams...")
live_stream = None

# Fetch live streams
print("Checking for specific live stream")
if config["LIVESTREAM_ID"] is not None and config["LIVESTREAM_ID"] != "":
    live_stream = get_live_stream(config["LIVESTREAM_ID"])

if live_stream is None:
    print("No live stream found from config. Fetching all live streams instead...")
    live_videos = get_live_streams(config["CHANNEL_ID"])
    live_stream = get_live_stream(live_videos[0]["video_id"])

# Print live stream information
if live_stream is not None:
    print(f"Live stream found: {live_stream["snippet"]['title']} | Link: https://www.youtube.com/watch?v={live_stream["id"]}")
else:
    print("No live streams found.")

# get chat id from live stream
live_chat_id = get_live_chat_id(live_stream["id"])

# Fetch live chat messages
print("Fetching live chat messages...")

while True:
    # sleep for 5 seconds
    get_new_live_chat_messages(live_chat_id)
    time.sleep(config["CHAT_UPDATE_INTERVAL_SECONDS"])
