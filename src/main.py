from youtube import get_live_streams, get_live_stream, get_new_live_chat_messages, get_live_chat_id
from config import config
from atlas import create_texture_atlas 
import time
import pygame
from pathlib import Path

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
# print("Fetching live chat messages...")

# while True:
#     # sleep for 5 seconds
#     messages = get_new_live_chat_messages(live_chat_id)
#     time.sleep(config["CHAT_UPDATE_INTERVAL_SECONDS"])

# Initialize texture atlas
def game():
    # Initialize pygame
    pygame.init()

    # Internal resolution (fixed size)
    INTERNAL_WIDTH, INTERNAL_HEIGHT = 1080, 1920

    # Start with a default window size (can be resized)
    WINDOW_WIDTH, WINDOW_HEIGHT = 540, 960  # Half of internal resolution

    BLOCK_SCALE_FACTOR = INTERNAL_WIDTH / 16 / 9;

    # Create a resizable window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Resizable Pygame Window")

    # Create an internal surface with fixed resolution
    internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))

    assets_dir = Path(__file__).parent.parent / "src/assets" 
    (texture_atlas, atlas_items) = create_texture_atlas(assets_dir)
    
    # Scale the entire texture atlas
    texture_atlas = pygame.transform.scale(texture_atlas, 
                                        (texture_atlas.get_width() * BLOCK_SCALE_FACTOR, 
                                        texture_atlas.get_height() * BLOCK_SCALE_FACTOR))

    for category in atlas_items:
        for item in atlas_items[category]:
            x, y, w, h = atlas_items[category][item]
            atlas_items[category][item] = (x * BLOCK_SCALE_FACTOR, y * BLOCK_SCALE_FACTOR, w * BLOCK_SCALE_FACTOR, h * BLOCK_SCALE_FACTOR)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Close window event
                running = False
            elif event.type == pygame.VIDEORESIZE:  # Window resize event
                new_width, new_height = event.w, event.h

                # Maintain 9:16 aspect ratio
                if new_width / 9 > new_height / 16:
                    new_width = int(new_height * (9 / 16))
                else:
                    new_height = int(new_width * (16 / 9))

                WINDOW_WIDTH, WINDOW_HEIGHT = new_width, new_height
                screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)


        # Fill internal surface with a color (e.g., dark gray)
        internal_surface.fill((30, 30, 30))

        # Draw the scaled atlas
        internal_surface.blit(texture_atlas, (0, 0), atlas_items["item"]["golden_pickaxe"])

        # Scale internal surface to fit the resized window
        scaled_surface = pygame.transform.smoothscale(internal_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Draw scaled surface onto the actual screen
        screen.blit(scaled_surface, (0, 0))
        # Update the display
        pygame.display.flip()

    # Quit pygame properly
    pygame.quit()

game()