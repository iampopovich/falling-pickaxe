import pygame
import pymunk
from constants import BLOCK_SIZE

class Block:
    def __init__(self, space, x, y, name, texture_atlas, atlas_items):
        if name == "bedrock":
            self.max_hp = 1000000000
            self.hp = 1000000000
        elif name == "stone":
            self.max_hp = 10
            self.hp = 10
        elif name == "andesite":
            self.hp = 10
            self.max_hp = 10
        elif name == "diorite":
            self.hp = 10
            self.max_hp = 10
        elif name == "granite":
            self.hp = 10
            self.max_hp = 10
        elif name == "coal_ore":
            self.hp = 15
            self.max_hp = 15
        elif name == "iron_ore":
            self.hp = 15
            self.max_hp = 15
        elif name == "gold_ore":
            self.hp = 20
            self.max_hp = 20
        elif name == "diamond_ore":
            self.hp = 20
            self.max_hp = 20
        elif name == "emerald_ore":
            self.hp = 20
            self.max_hp = 20
        elif name == "obsidian":
            self.hp = 100
            self.max_hp = 100
        elif name == "redstone_ore":
            self.hp = 15
            self.max_hp = 15
        elif name == "lapis_ore":
            self.hp = 15
            self.max_hp = 15
        elif name == "mossy_cobblestone":
            self.hp = 12
            self.max_hp = 12
        elif name == "cobblestone":
            self.hp = 22
            self.max_hp = 22
        else:
            self.hp = 1
            self.max_hp = 1

        self.texture_atlas = texture_atlas
        self.atlas_items = atlas_items

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

        # Determine the destroy stage (0-9) based on hp percentage
        if self.hp < self.max_hp:
            damage_stage = int((1 - (self.hp / self.max_hp)) * 9)  # Scale hp to 0-9 range
            damage_stage = min(damage_stage, 9)  # Ensure it doesn't exceed stage_9
            
            # Draw the destroy stage overlay
            destroy_texture = self.texture_atlas.subsurface(
                self.atlas_items["destroy_stage"][f"destroy_stage_{damage_stage}"]
            )
            screen.blit(destroy_texture, (block_x, block_y))