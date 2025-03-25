import pygame
import pymunk
import pymunk.pygame_util

class Pickaxe:
    def __init__(self, space, x, y, texture):
        self.texture = texture
        width, height = self.texture.get_size()

        # Create physics body
        self.body = pymunk.Body()
        self.body.position = (x, y)

        # Create shape (hitbox) based on texture size
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.density = 1  # Affects gravity
        self.shape.elasticity = 0.5  # Bounciness
        space.add(self.body, self.shape)  # Add to physics world

    def update(self):
        """ Update pickaxe physics (handled by pymunk) """
        pass  # Pymunk automatically updates the physics

    def draw(self, screen):
        """ Draw rotated pickaxe at physics body's position """
        angle = -self.body.angle * 57.2958  # Convert radians to degrees
        rotated_image = pygame.transform.rotate(self.texture, angle)
        rect = rotated_image.get_rect(center=self.body.position)
        screen.blit(rotated_image, rect.topleft)
