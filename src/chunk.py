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
    if(chunk_x % 10 == 0 and chunk_y % 10 == 0):
        return generate_empty_chunk()

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

def clean_chunks(start_chunk_y):
    for (chunk_x, chunk_y) in list(chunks.keys()):
        if chunk_y < start_chunk_y:
            del chunks[(chunk_x, chunk_y)]