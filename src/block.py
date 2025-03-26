import pygame
import pymunk
from constants import BLOCK_SIZE

class Block:
    def __init__(self, space, x, y, name, texture_atlas, atlas_items):
        if(name == "bedrock"):
            self.hp = 1000000000
        else:
            self.hp = 100

        rect = atlas_items["block"][name]  
        self.texture = texture_atlas.subsurface(rect)

        width, height = self.texture.get_size()

        # Create a static physics body (doesn't move)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x + BLOCK_SIZE//2, y + BLOCK_SIZE//2)

        # Create a hitbox
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 1  # No bounce
        self.shape.collision_type = 1  # Identifier for collisions
        self.shape.friction = 1

        space.add(self.body, self.shape)

        # print("Block created at", self.body.position, "with texture", name) 

    def take_damage(self, amount):
        """Reduce HP when hit"""
        self.hp -= amount
        if self.hp <= 0:
            self.space.remove(self.body, self.shape)
            return True  # Block should be destroyed
        return False

    def draw(self, screen, camera):
        """Draw block at its position"""
        block_x = self.body.position.x - BLOCK_SIZE // 2
        block_y = self.body.position.y - camera.offset_y - BLOCK_SIZE // 2

        screen.blit(self.texture, (block_x, block_y))

        # Draw the polygon hitbox for better representation
        vertices = self.shape.get_vertices()
        vertices = [(v.x + self.body.position.x, v.y + self.body.position.y - camera.offset_y) for v in vertices]
        pygame.draw.polygon(screen, (255, 0, 0), vertices, 2)


