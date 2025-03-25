import pygame
import noise  # For procedural generation
import random
from block import Block
from constants import BLOCK_SIZE, CHUNK_HEIGHT, CHUNK_WIDTH, SEED

def generate_empty_chunk(texture_atlas, atlas_items, space): 
    chunk = []
    for y in range(CHUNK_HEIGHT):
        row = []
        for x in range(CHUNK_WIDTH):
            if(x == 0 or x == CHUNK_WIDTH - 1):
                block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
                block_y = (0 * CHUNK_HEIGHT + y) * BLOCK_SIZE
                row.append(Block(space, block_x, block_y, "bedrock", texture_atlas, atlas_items))
                continue
            
            row.append(None)
        chunk.append(row)
    return chunk

# Function to generate chunks using Perlin noise
def generate_chunk(chunk_x, chunk_y, texture_atlas, atlas_items, space):
    if(chunk_x == 0 and chunk_y == 0):
        return generate_empty_chunk(texture_atlas, atlas_items, space)

    chunk = []
    for y in range(CHUNK_HEIGHT):
        row = []
        for x in range(CHUNK_WIDTH):
            block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
            block_y = (chunk_y * CHUNK_HEIGHT + y) * BLOCK_SIZE

            if(x == 0 or x == CHUNK_WIDTH - 1):
                row.append(Block(space, block_x, block_y, "bedrock", texture_atlas, atlas_items))
                continue

            noise_value = noise.pnoise2(
                (chunk_x * CHUNK_WIDTH + x) * 0.1,  # Horizontal variation
                (chunk_y * CHUNK_HEIGHT + y) * 0.1,  # Vertical variation
                octaves=4, persistence=0.5, lacunarity=2.0, repeatx=9999, repeaty=9999, base=SEED
            )

            # Block selection based on noise value
            if noise_value < -0.2:
                row.append(Block(space, block_x, block_y, "stone", texture_atlas,atlas_items))
            elif noise_value < 0.1:
                row.append(Block(space, block_x, block_y, "dirt", texture_atlas,atlas_items))
            else:
                row.append(Block(space, block_x, block_y, "cobblestone", texture_atlas,atlas_items))
        chunk.append(row)
    return chunk

# Store generated chunks
chunks = {}

def get_block(chunk_x, chunk_y, x, y, texture_atlas, atlas_items, space):
    if (chunk_x, chunk_y) not in chunks:
        print("Generating chunk", chunk_x, chunk_y) 
        chunks[(chunk_x, chunk_y)] = generate_chunk(chunk_x, chunk_y, texture_atlas, atlas_items, space)

    return chunks[(chunk_x, chunk_y)][y][x]

def delete_block(chunk_x, chunk_y, x, y):
    if (chunk_x, chunk_y) in chunks:
        chunks[(chunk_x, chunk_y)][y][x] = None

def clean_chunks(start_chunk_y):
    for (chunk_x, chunk_y) in list(chunks.keys()):
        if chunk_y < start_chunk_y:
            del chunks[(chunk_x, chunk_y)]