import pygame
from constants import BLOCK_SIZE, CHUNK_HEIGHT


class Hud:
    def __init__(self, texture_atlas, atlas_items, position=(32, 32)):
        """
        :param texture_atlas: The atlas surface containing the item icons.
        :param atlas_items: A dict with keys under "item" for each ore.
        :param position: Top-left position where the HUD will be drawn.
        """
        self.texture_atlas = texture_atlas
        self.atlas_items = atlas_items

        # Initialize ore amounts to 0.
        self.amounts = {
            "coal": 0,
            "iron_ingot": 0,
            "copper_ingot": 0,
            "gold_ingot": 0,
            "redstone": 0,
            "lapis_lazuli": 0,
            "diamond": 0,
            "emerald": 0,
        }

        self.position = position
        self.icon_size = (64, 64)  # Size to draw each icon
        self.spacing = 15  # Space between items

        # Initialize a font (using the default font and size 24)
        self.font = pygame.font.Font(None, 64)

    def update_amounts(self, new_amounts):
        """
        Update the ore amounts.
        :param new_amounts: Dict with ore names as keys and integer amounts as values.
        """
        self.amounts.update(new_amounts)

    def draw(self, screen, pickaxe_y, fast_slow_active, fast_slow):
        """
        Draws the HUD: each ore icon with its amount.
        """
        x, y = self.position

        for ore, amount in self.amounts.items():
            # Retrieve the icon rect from atlas_items["item"][ore]
            if ore in self.atlas_items["item"]:
                icon_rect = pygame.Rect(self.atlas_items["item"][ore])
                icon = self.texture_atlas.subsurface(icon_rect)
                # Scale the icon to desired icon size
                icon = pygame.transform.scale(icon, self.icon_size)
                # Blit the icon
                screen.blit(icon, (x, y))
            else:
                # In case the ore key is missing, skip drawing the icon
                continue

            # Render the amount text
            text_surface = self.font.render(str(amount), True, (255, 255, 255))
            # Position text to the right of the icon
            text_x = x + self.icon_size[0] + self.spacing
            text_y = y + (self.icon_size[1] - text_surface.get_height()) // 2 + 3
            screen.blit(text_surface, (text_x, text_y))

            # Move to the next line
            y += self.icon_size[1] + self.spacing

        # Draw the pickaxe position indicator
        pickaxe_indicator_x = x + self.spacing
        pickaxe_indicator_y = y + self.spacing
        pickaxe_indicator_surface = self.font.render(f"Y: {-int(pickaxe_y // BLOCK_SIZE)}", True, (255, 255, 255))
        screen.blit(pickaxe_indicator_surface, (pickaxe_indicator_x, pickaxe_indicator_y))

        # Draw the fast/slow indicator
        if fast_slow_active:
            fast_slow_surface = self.font.render(f"{fast_slow}", True, (255, 255, 255))
            fast_slow_x = x + self.spacing
            fast_slow_y = y + 2 * self.spacing + fast_slow_surface.get_height()
            screen.blit(fast_slow_surface, (fast_slow_x, fast_slow_y))
        else:
            fast_slow_surface = self.font.render("Normal", True, (255, 255, 255))
            fast_slow_x = x + self.spacing
            fast_slow_y = y + 2 * self.spacing + fast_slow_surface.get_height()
            screen.blit(fast_slow_surface, (fast_slow_x, fast_slow_y))

        

