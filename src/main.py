import time
import pygame
import pymunk
import pymunk.pygame_util   
from youtube import get_live_streams, get_live_stream, get_new_live_chat_messages, get_live_chat_id
from config import config
from atlas import create_texture_atlas 
from pathlib import Path
from chunk import get_block, clean_chunks, delete_block, chunks
from constants import BLOCK_SCALE_FACTOR, BLOCK_SIZE, CHUNK_HEIGHT, CHUNK_WIDTH, INTERNAL_HEIGHT, INTERNAL_WIDTH
from pickaxe import Pickaxe
from camera import Camera
from sound import SoundManager
from tnt import Tnt
import random
from hud import Hud

# print("Fetching live streams...")
# live_stream = None

# # Fetch live streams
# print("Checking for specific live stream")
# if config["LIVESTREAM_ID"] is not None and config["LIVESTREAM_ID"] != "":
#     live_stream = get_live_stream(config["LIVESTREAM_ID"])

# if live_stream is None:
#     print("No live stream found from config. Fetching all live streams instead...")
#     live_videos = get_live_streams(config["CHANNEL_ID"])
#     live_stream = get_live_stream(live_videos[0]["video_id"])

# # Print live stream information
# if live_stream is not None:
#     print(f"Live stream found: {live_stream["snippet"]['title']} | Link: https://www.youtube.com/watch?v={live_stream["id"]}")
# else:
#     print("No live streams found.")

# # get chat id from live stream
# live_chat_id = get_live_chat_id(live_stream["id"])

# Fetch live chat messages
# print("Fetching live chat messages...")

# while True:
#     # sleep for 5 seconds
#     messages = get_new_live_chat_messages(live_chat_id)
#     time.sleep(config["CHAT_UPDATE_INTERVAL_SECONDS"])

# Initialize texture atlas


def game():
    WINDOW_WIDTH, WINDOW_HEIGHT = 540, 960  # Half of internal resolution
    
    # Initialize pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Pymunk physics 
    space = pymunk.Space()
    space.gravity = (0, 1000)  # (x, y) - down is positive y

    # Create a resizable window
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Falling Pickaxe")
    # set icon
    icon = pygame.image.load(Path(__file__).parent.parent / "src/assets/pickaxe" / "diamond_pickaxe.png")
    pygame.display.set_icon(icon)

    # Create an internal surface with fixed resolution
    internal_surface = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))

    # Load texture atlas
    assets_dir = Path(__file__).parent.parent / "src/assets" 
    (texture_atlas, atlas_items) = create_texture_atlas(assets_dir)
    
    # Load background 
    background_image = pygame.image.load(assets_dir / "background.png")
    background_scale_factor = 1.5  
    background_width = int(background_image.get_width() * background_scale_factor)
    background_height = int(background_image.get_height() * background_scale_factor)
    background_image = pygame.transform.scale(background_image, (background_width, background_height))

    # Scale the entire texture atlas
    texture_atlas = pygame.transform.scale(texture_atlas, 
                                        (texture_atlas.get_width() * BLOCK_SCALE_FACTOR, 
                                        texture_atlas.get_height() * BLOCK_SCALE_FACTOR))

    for category in atlas_items:
        for item in atlas_items[category]:
            x, y, w, h = atlas_items[category][item]
            atlas_items[category][item] = (x * BLOCK_SCALE_FACTOR, y * BLOCK_SCALE_FACTOR, w * BLOCK_SCALE_FACTOR, h * BLOCK_SCALE_FACTOR)

    #sounds 
    sound_manager = SoundManager()

    sound_manager.load_sound("tnt", assets_dir / "sounds" / "tnt.mp3", 0.3)
    sound_manager.load_sound("stone1", assets_dir / "sounds" / "stone1.wav", 0.5)
    sound_manager.load_sound("stone2", assets_dir / "sounds" / "stone2.wav", 0.5)
    sound_manager.load_sound("stone3", assets_dir / "sounds" / "stone3.wav", 0.5)
    sound_manager.load_sound("stone4", assets_dir / "sounds" / "stone4.wav", 0.5)
    sound_manager.load_sound("grass1", assets_dir / "sounds" / "grass1.wav", 0.1)
    sound_manager.load_sound("grass2", assets_dir / "sounds" / "grass2.wav", 0.1)
    sound_manager.load_sound("grass3", assets_dir / "sounds" / "grass3.wav", 0.1)
    sound_manager.load_sound("grass4", assets_dir / "sounds" / "grass4.wav", 0.1)

    # Pickaxe
    pickaxe = Pickaxe(space, INTERNAL_WIDTH // 2, INTERNAL_HEIGHT // 2, texture_atlas.subsurface(atlas_items["pickaxe"]["diamond_pickaxe"]), sound_manager)

    # TNT
    last_tnt_spawn = pygame.time.get_ticks()
    tnt_spawn_interval = 1000 * random.uniform(config["TNT_SPAWN_INTERVAL_SECONDS_MIN"], config["TNT_SPAWN_INTERVAL_SECONDS_MAX"]) 
    tnt_list = []  # List to keep track of spawned TNT objects

    # Camera
    camera = Camera()

    # HUD
    hud = Hud(texture_atlas, atlas_items)

    # Explosions
    explosions = []

    # Main loop
    running = True
    while running:
        # ++++++++++++++++++  EVENTS ++++++++++++++++++ 
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

        # ++++++++++++++++++  UPDATE ++++++++++++++++++
        # Determine which chunks are visible
        # Update physics
        space.step(1 / 60.0) 

        start_chunk_y = int(pickaxe.body.position.y // (CHUNK_HEIGHT * BLOCK_SIZE) - 1)
        end_chunk_y = int(pickaxe.body.position.y + INTERNAL_HEIGHT) // (CHUNK_HEIGHT * BLOCK_SIZE)  + 1

        # Update pickaxe
        pickaxe.update()

        # Update camera
        camera.update(pickaxe.body.position.y)

        # ++++++++++++++++++  DRAWING ++++++++++++++++++
        # Clear the internal surface
        screen.fill((0, 0, 0))

        # Fill internal surface with the background
        internal_surface.blit(background_image, ((INTERNAL_WIDTH - background_width) // 2, (INTERNAL_HEIGHT - background_height) // 2))

        # Check if it's time to spawn a new TNT
        current_time = pygame.time.get_ticks()
        if current_time - last_tnt_spawn >= tnt_spawn_interval:
            # Example: spawn TNT at position (400, 300) with a given texture
            new_tnt = Tnt(space, pickaxe.body.position.x, pickaxe.body.position.y - 100, texture_atlas, atlas_items, sound_manager)
            tnt_list.append(new_tnt)
            last_tnt_spawn = current_time
            # New random interval for the next TNT spawn
            tnt_spawn_interval = 1000 * random.uniform(config["TNT_SPAWN_INTERVAL_SECONDS_MIN"], config["TNT_SPAWN_INTERVAL_SECONDS_MAX"]) 

        # Update and draw all TNT objects
        for tnt in tnt_list:
            tnt.update(tnt_list, explosions)
        
        # Delete chunks 
        clean_chunks(start_chunk_y)

        # Draw blocks in visible chunks
        for chunk_y in range(start_chunk_y, end_chunk_y):
            for y in range(CHUNK_HEIGHT):
                for x in range(CHUNK_WIDTH):
                    block = get_block(0, chunk_y, x, y, texture_atlas, atlas_items, space)
                    
                    if block == None:
                        continue
                    
                    block.update(space, hud)
                    block.draw(internal_surface, camera)

        # Draw pickaxe
        pickaxe.draw(internal_surface, camera)

        # Draw TNT
        for tnt in tnt_list:
            tnt.draw(internal_surface, camera)

        # Draw particles
        for explosion in explosions:
            explosion.update()
            explosion.draw(internal_surface, camera)
            
        # Optionally, remove explosions that have no particles left:
        explosions = [e for e in explosions if e.particles]

        # Draw HUD
        hud.draw(internal_surface)

        # Scale internal surface to fit the resized window
        scaled_surface = pygame.transform.smoothscale(internal_surface, (WINDOW_WIDTH, WINDOW_HEIGHT))
        screen.blit(scaled_surface, (0, 0))

        # Update the display
        pygame.display.flip()
        clock.tick(50)  # Cap the frame rate
    # Quit pygame properly
    pygame.quit()

game()

# check if pickaxe is outside the screen