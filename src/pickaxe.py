import pygame
import math

class Pickaxe:
    def __init__(self, x, y, texture, velocity=0, gravity=0.5, rotation=0):
        self.x = x
        self.y = y
        self.texture = texture
        self.velocity = velocity
        self.gravity = gravity
        self.rotation = rotation
        self.angular_velocity = 0  # Rotation speed
        self.hitbox = self.get_hitbox()
        self.terminal_velocity = 100  # Maximum falling speed

    def get_hitbox(self):
        """Return a rotated hitbox using the pickaxe shape."""
        rotated_image = pygame.transform.rotate(self.texture, self.rotation)
        return rotated_image.get_rect(center=(self.x, self.y))

    def update(self):
        """Apply gravity, update movement, check collisions, and rotate."""
        self.velocity += self.gravity  # Gravity affects velocity
        self.y += self.velocity  # Apply velocity to position
        self.rotation += self.angular_velocity  # Apply angular velocity
        self.hitbox = self.get_hitbox()  # Update hitbox

        if (self.velocity > self.terminal_velocity):
            self.velocity = self.terminal_velocity

    def draw(self, screen, camera):
        """Draw the rotated pickaxe at its current position."""
        rotated_image = pygame.transform.rotate(self.texture, self.rotation)
        rect = rotated_image.get_rect(center=(self.x, self.y))
        rect.y -= camera.offset_y
        screen.blit(rotated_image, rect)

        # Adjust hitbox position for camera before drawing
        adjusted_hitbox = self.hitbox.copy()
        adjusted_hitbox.y -= camera.offset_y  
        pygame.draw.rect(screen, (255, 0, 0), adjusted_hitbox, 2)  # Draw adjusted hitbox
