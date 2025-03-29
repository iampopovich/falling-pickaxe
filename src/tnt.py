import pygame
import pymunk
import math
import random
from constants import BLOCK_SIZE
from chunk import chunks
from explosion import Explosion

class Tnt:
    def __init__(self, space, x, y, texture_atlas, atlas_items, sound_manager, velocity=0, rotation=0, mass=70):
        print("Spawning TNT")
        self.texture_atlas = texture_atlas
        self.atlas_items = atlas_items

        rect = atlas_items["block"]["tnt"]  
        self.texture = texture_atlas.subsurface(rect)

        width, height = self.texture.get_size()

        self.name = "tnt"

        self.velocity = velocity
        self.rotation = rotation
        self.space = space

        inertia = pymunk.moment_for_box(mass, (width, height))
        self.body = pymunk.Body(mass, inertia)
        self.body.position = (x, y)
        self.body.angle = math.radians(rotation)

        # Create a hitbox
        self.shape = pymunk.Poly.create_box(self.body, (width, height))
        self.shape.elasticity = 1  # No bounce
        self.shape.collision_type = 3 # Identifier for collisions
        self.shape.friction = 0.7
        self.shape.block_ref = self  # Reference to the block object

        self.sound_manager = sound_manager

        sound_manager.play_sound("tnt")

        self.space.add(self.body, self.shape)

        # Add collision handler for pickaxe & blocks
        handler = space.add_collision_handler(3, 2)  # (Pickaxe type, Block type)
        handler.post_solve = self.on_collision

        self.detonated = False
        self.spawn_time = pygame.time.get_ticks()

    def on_collision(self, arbiter, space, data):
        """Handles collision with blocks: Reduce HP or destroy the block."""

        # Add small random rotation on hit
        self.body.angle += random.choice([0.01, -0.01])

    def explode(self, explosions):
        explosion_radius = 3 * BLOCK_SIZE  # Explosion radius in pixels
        self.detonated = True

        # Iterate over all chunks
        for chunk in chunks:
            for row in chunks[chunk]:
                for block in row:
                    # Skip blocks that might already be destroyed
                    if block is None or getattr(block, "destroyed", False):
                        continue

                    # Calculate distance from TNT to block center
                    dx = block.body.position.x - self.body.position.x
                    dy = block.body.position.y - self.body.position.y
                    distance = math.hypot(dx, dy)

                    # If the block is within the explosion radius, damage it
                    if distance <= explosion_radius:
                        # Calculate damage as a function of distance
                        # Full damage at the center, decreasing linearly to 0 at explosion_radius
                        damage = int(100 * (1 - (distance / explosion_radius)))
                        # Apply the damage (using block.take_damage if you have such a method,
                        # or directly reducing block.hp)
                        block.hp -= damage

        explosion = Explosion(self.body.position, self.texture_atlas, self.atlas_items, particle_count=20)
        explosions.append(explosion)

    def update(self, tnt_list, explosions):
        """Update TNT physics like gravity and rotation."""
        if self.detonated:
            self.space.remove(self.body, self.shape)
            tnt_list.remove(self)
            return
        
        # Limit falling speed (terminal velocity)
        if self.body.velocity.y > 1000:
            self.body.velocity = (self.body.velocity.x, 1000)

        # after 4 seconds, explode
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time >= 4000:
            self.explode(explosions)

    def draw(self, screen, camera):
        """Draw the TNT at its current position with a blinking white overlay that respects rotation."""

        if self.detonated:
            return

        # Rotate the TNT texture and get its rect
        rotated_image = pygame.transform.rotate(self.texture, -math.degrees(self.body.angle))
        rect = rotated_image.get_rect(center=(self.body.position.x, self.body.position.y))
        rect.y -= camera.offset_y
        screen.blit(rotated_image, rect)

        # Blinking effect: Compute a pulsating alpha using a sine wave.
        blink_period = 500  # 1 second cycle
        current_time = pygame.time.get_ticks() % blink_period
        brightness = (math.sin(current_time / blink_period * 2 * math.pi) + 1) / 2  # range 0-1
        alpha = int(brightness * 192)  # maximum 50% opacity

        # Create a white overlay at the original texture size with per-pixel alpha
        white_overlay = pygame.Surface(self.texture.get_size(), pygame.SRCALPHA)
        white_overlay.fill((255, 255, 255, alpha))
        
        # Rotate the white overlay using the same angle as the TNT
        rotated_overlay = pygame.transform.rotate(white_overlay, -math.degrees(self.body.angle))
        overlay_rect = rotated_overlay.get_rect(center=(self.body.position.x, self.body.position.y))
        overlay_rect.y -= camera.offset_y

        # Blit the rotated overlay on top of the TNT
        screen.blit(rotated_overlay, overlay_rect)
