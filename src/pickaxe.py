import pygame
import math
import pymunk
import pymunk.autogeometry
from chunk import chunks
from constants import BLOCK_SIZE
import random

def rotate_point(x, y, angle):
    """Rotate a point (x, y) by angle (in radians) around the origin (0, 0)."""
    cos_angle = math.cos(angle)
    sin_angle = math.sin(angle)
    new_x = cos_angle * x - sin_angle * y
    new_y = sin_angle * x + cos_angle * y
    return new_x, new_y

def rotate_vertices(vertices, angle):
        rotated_vertices = []

        for vertex in vertices:
            # Rotate each vertex based on the body's angle
            rotated_x, rotated_y = rotate_point(vertex[0] - BLOCK_SIZE / 2 , vertex[1] - BLOCK_SIZE / 2, angle)

            # Offset each rotated vertex by the body's position
            rotated_vertices.append((rotated_x, rotated_y))
        
        return rotated_vertices

class Pickaxe:
    def __init__(self, space, x, y, texture, velocity=0, rotation=0, mass=100):
        self.texture = texture
        self.velocity = velocity
        self.rotation = rotation
        self.space = space

        vertices = rotate_vertices([
                    (0, 0), # A
                    (10, 0), # C
                    (110, 100), # D
                    (100, 110), # E
                    (0, 10), # F
                    (110, 110), # G
                ], -math.pi / 2)
        
        vertices2 = rotate_vertices([
                    (110, 30), # H
                    (120, 40), # I
                    (120, 90), # J
                    (100, 90), # K
                    (100, 40), # L
                    (110, 100), # D
                ], -math.pi / 2)
        
        vertices3 = rotate_vertices([
                    (30, 110), # M
                    (40, 120), # N
                    (90, 120), # O
                    (40, 100), # P
                    (90, 100), # Q
                    (100, 110), # E
                ], -math.pi / 2)

        inertia = pymunk.moment_for_poly(mass, vertices)
        self.body = pymunk.Body(mass, inertia)
        self.body.position = (x, y)
        self.body.angle = math.radians(rotation)

        self.shapes = []
        for vertices in [vertices, vertices2, vertices3]:
            shape = pymunk.Poly(self.body, vertices)
            shape.elasticity = 0.7
            shape.friction = 0.7
            self.shapes.append(shape)

        self.space.add(self.body, *self.shapes)

    def update(self):
        """Apply gravity, update movement, check collisions, and rotate."""
        # Manually limit the falling speed (terminal velocity)
        if self.body.velocity.y > 1000:
            self.body.velocity = (self.body.velocity.x, 1000)

        # Add a bit of random rotation on hit 
        #if(self.body.velocity.y == 0):
        #    self.body.angle += random.choice([0.01, -0.01])


    def draw(self, screen, camera):
        """Draw the pickaxe at its current position."""
        rotated_image = pygame.transform.rotate(self.texture, -math.degrees(self.body.angle))  # Convert to degrees
        rect = rotated_image.get_rect(center=(self.body.position.x, self.body.position.y))
        rect.y -= camera.offset_y
        screen.blit(rotated_image, rect)


        for shape in self.shapes:
        # Draw the polygon hitbox for better representation
            vertices = shape.get_vertices()
            # Rotate and offset each vertex
            rotated_vertices = []
            for vertex in vertices:
                # Rotate each vertex based on the body's angle
                rotated_x, rotated_y = rotate_point(vertex[0], vertex[1], self.body.angle)

                # Offset each rotated vertex by the body's position
                rotated_vertices.append((rotated_x + self.body.position.x, rotated_y + self.body.position.y - camera.offset_y))

            # Draw the polygon hitbox for better representation
            pygame.draw.polygon(screen, (255, 0, 0), rotated_vertices, 2)  # Draw the hitbox outline

        # # Optionally, draw the mask (pixel-perfect collision)
        # mask_surface = self.mask.to_surface(setcolor=(255, 0, 0), unsetcolor=(0, 0, 0, 0))
        # screen.blit(mask_surface, rect)