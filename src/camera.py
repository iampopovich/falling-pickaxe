import pygame
from constants import INTERNAL_HEIGHT, CHUNK_HEIGHT, BLOCK_SIZE

class Camera:
    def __init__(self):
        self.offset_y = 0  # Vertical offset

    def update(self, target_y):
        """Follow the pickaxe smoothly"""
        self.offset_y = target_y - INTERNAL_HEIGHT // 2  # Center the pickaxe
