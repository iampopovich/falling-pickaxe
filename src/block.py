import pygame
import pymunk
from constants import BLOCK_SIZE

class Block:
    def __init__(self, space, x, y, name, texture_atlas, atlas_items):
        if(name == "bedrock"):
            self.hp = 1000000000
        elif(name == "stone"):
            self.hp = 50
        elif(name == "dirt"):
            self.hp = 1
        elif(name == "cobblestone"):
            self.hp = 30
        else:
            self.hp = 1

        rect = atlas_items["block"][name]  
        self.texture = texture_atlas.subsurface(rect)

        width, height = self.texture.get_size()

        # Create a static physics body (doesn't move)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2)

        # Create a hitbox
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 1  # No bounce
        self.shape.collision_type = 2 # Identifier for collisions
        self.shape.friction = 1
        self.shape.block_ref = self  # Reference to the block object

        self.destroyed = False

        space.add(self.body, self.shape)

    def draw(self, screen, camera):
        """Draw block at its position"""

        if(self.destroyed):
            return

        block_x = self.body.position.x - BLOCK_SIZE // 2
        block_y = self.body.position.y - camera.offset_y - BLOCK_SIZE // 2

        screen.blit(self.texture, (block_x, block_y))

