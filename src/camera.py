import pygame
from constants import INTERNAL_HEIGHT

class Camera:
    def __init__(self):
        self.offset_y = 0  # Vertical offset

    def update(self, target_y, smoothing=0.1):
        """Smoothly follow the target's y position (e.g., pickaxe)"""
        # Desired offset centers the target in the middle of the screen
        desired_offset = target_y - INTERNAL_HEIGHT // 2
        
        # Interpolate between current offset and desired offset
        self.offset_y += (desired_offset - self.offset_y) * smoothing
