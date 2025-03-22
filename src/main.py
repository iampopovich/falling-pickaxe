from youtube import get_live_streams, get_live_stream
from config import config 

# Fetch live streams
live_videos = get_live_streams(config["CHANNEL_ID"])
live_stream = get_live_stream(live_videos[0]["video_id"])


