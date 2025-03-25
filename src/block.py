import pygame
import pymunk

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
        self.body.position = (x, y)

        # Create a hitbox
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 0  # No bounce
        self.shape.collision_type = 1  # Identifier for collisions

        space.add(self.body, self.shape)

        # print("Block created at", self.body.position, "with texture", name) 

    def take_damage(self, amount):
        """Reduce HP when hit"""
        self.hp -= amount
        if self.hp <= 0:
            return True  # Block should be destroyed
        return False

    def draw(self, screen):
        """Draw block at its position"""
        rect = self.texture.get_rect(center=self.body.position)
        screen.blit(self.texture, self.body.position)
