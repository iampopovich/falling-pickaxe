import pygame
import noise  # For procedural generation
import random

# Constants
CHUNK_WIDTH = 9  # Number of blocks per chunk width
CHUNK_HEIGHT = 16  # Number of blocks per chunk height
SEED = 12345  # Fixed seed for world consistency

# Block textures (for testing)
BLOCK_COLORS = {
    "stone": (100, 100, 100),
    "dirt": (120, 80, 50),
    "grass": (50, 200, 50),
    "bedrock": (50, 50, 50)
}

def generate_empty_chunk(): 
    chunk = []
    for y in range(CHUNK_HEIGHT):
        row = []
        for x in range(CHUNK_WIDTH):
            if(x == 0 or x == CHUNK_WIDTH - 1):
                row.append("bedrock")
                continue
            
            row.append("")
        chunk.append(row)
    return chunk

# Function to generate chunks using Perlin noise
def generate_chunk(chunk_x, chunk_y):
    chunk = []
    for y in range(CHUNK_HEIGHT):
        row = []
        for x in range(CHUNK_WIDTH):
            if(x == 0 or x == CHUNK_WIDTH - 1):
                row.append("bedrock")
                continue

            noise_value = noise.pnoise2(
                (chunk_x * CHUNK_WIDTH + x) * 0.1,  # Horizontal variation
                (chunk_y * CHUNK_HEIGHT + y) * 0.1,  # Vertical variation
                octaves=4, persistence=0.5, lacunarity=2.0, repeatx=9999, repeaty=9999, base=SEED
            )

            # Block selection based on noise value
            if noise_value < -0.2:
                row.append("stone")
            elif noise_value < 0.1:
                row.append("dirt")
            else:
                row.append("grass")
        chunk.append(row)
    return chunk

# Store generated chunks
chunks = {}

def get_block(chunk_x, chunk_y, x, y):
    if (chunk_x, chunk_y) not in chunks:
        chunks[(chunk_x, chunk_y)] = generate_chunk(chunk_x, chunk_y)

    return chunks[(chunk_x, chunk_y)][y][x]

# Game loop
running = True
while running:
    screen.fill((135, 206, 235))  # Sky color

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Determine which chunks are visible
    start_chunk_y = player_y // (CHUNK_HEIGHT * BLOCK_SIZE)
    end_chunk_y = (player_y + SCREEN_HEIGHT) // (CHUNK_HEIGHT * BLOCK_SIZE)

    for chunk_y in range(start_chunk_y, end_chunk_y + 1):
        for chunk_x in range(-1, 2):  # Load chunks around the player horizontally
            for y in range(CHUNK_HEIGHT):
                for x in range(CHUNK_WIDTH):
                    block_type = get_block(chunk_x, chunk_y, x, y)
                    block_color = BLOCK_COLORS[block_type]
                    block_x = (chunk_x * CHUNK_WIDTH + x) * BLOCK_SIZE
                    block_y = (chunk_y * CHUNK_HEIGHT + y) * BLOCK_SIZE - player_y
                    pygame.draw.rect(screen, block_color, (block_x, block_y, BLOCK_SIZE, BLOCK_SIZE))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
