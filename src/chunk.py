import pygame
import noise  # For procedural generation
import random
from block import Block
from constants import BLOCK_SIZE, CHUNK_HEIGHT, CHUNK_WIDTH, SEED

def generate_first_chunk(texture_atlas, atlas_items, space): 
    chunk = []
    for y in range(CHUNK_HEIGHT):
        row = []
        for x in range(CHUNK_WIDTH):
            if(x == 0 or x == CHUNK_WIDTH - 1):
                block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
                block_y = (0 * CHUNK_HEIGHT + y) * BLOCK_SIZE
                row.append(Block(space, block_x, block_y, "bedrock", texture_atlas, atlas_items))
                continue
            elif y == 0:
                block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
                block_y = (0 * CHUNK_HEIGHT + y) * BLOCK_SIZE
                row.append(Block(space, block_x, block_y, "bedrock", texture_atlas, atlas_items))
                continue
            elif y == CHUNK_HEIGHT - 2:
                block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
                block_y = (0 * CHUNK_HEIGHT + y) * BLOCK_SIZE
                row.append(Block(space, block_x, block_y, "grass_block_side", texture_atlas, atlas_items))
                continue
            elif y == CHUNK_HEIGHT - 1:
                block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
                block_y = (0 * CHUNK_HEIGHT + y) * BLOCK_SIZE
                row.append(Block(space, block_x, block_y, "dirt", texture_atlas, atlas_items))
                continue
            row.append(None)
        chunk.append(row)
    return chunk

# Function to generate chunks using Perlin noise
def generate_chunk(chunk_x, chunk_y, texture_atlas, atlas_items, space):
    if(chunk_y <= 0):
        return generate_first_chunk(texture_atlas, atlas_items, space)

    chunk = []
    for y in range(CHUNK_HEIGHT):
        row = []
        for x in range(CHUNK_WIDTH):
            block_x = (0 * CHUNK_WIDTH + x) * BLOCK_SIZE
            block_y = (chunk_y * CHUNK_HEIGHT + y) * BLOCK_SIZE

            if(x == 0 or x == CHUNK_WIDTH - 1):
                row.append(Block(space, block_x, block_y, "bedrock", texture_atlas, atlas_items))
                continue

            noise_value = random.uniform(-1, 1)

            # Block selection based on noise value
            if noise_value < -0.4:
                row.append(Block(space, block_x, block_y, "andesite", texture_atlas, atlas_items))  # Deep layers
            elif noise_value < -0.2:
                row.append(Block(space, block_x, block_y, "stone", texture_atlas, atlas_items))  # Deeper layers
            elif noise_value < 0.0:
                row.append(Block(space, block_x, block_y, "coal_ore", texture_atlas, atlas_items))  # Middle layers
            elif noise_value < 0.3:
                row.append(Block(space, block_x, block_y, "diamond_ore", texture_atlas, atlas_items))  # Surface layer
            else:
                row.append(Block(space, block_x, block_y, "cobblestone", texture_atlas, atlas_items))  # Hills/rocky areas

        chunk.append(row)
    return chunk

# Store generated chunks
chunks = {}

def get_block(chunk_x, chunk_y, x, y, texture_atlas, atlas_items, space):
    if (chunk_x, chunk_y) not in chunks:
        chunks[(chunk_x, chunk_y)] = generate_chunk(chunk_x, chunk_y, texture_atlas, atlas_items, space)

    return chunks[(chunk_x, chunk_y)][y][x]

def delete_block(chunk_x, chunk_y, x, y):
    if (chunk_x, chunk_y) in chunks:
        chunks[(chunk_x, chunk_y)][y][x] = None

def clean_chunks(start_chunk_y):
    for (chunk_x, chunk_y) in list(chunks.keys()):
        if chunk_y < start_chunk_y:
            del chunks[(chunk_x, chunk_y)]