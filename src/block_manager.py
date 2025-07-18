import pygame
from typing import Dict, Set, List, Tuple
from block import Block
from constants import BLOCK_SIZE, CHUNK_HEIGHT, CHUNK_WIDTH

class BlockManager:
    """
    Optimized block manager for significant performance improvement.

    Main optimizations:
    1. "Dirty" block system - only update changed blocks
    2. Separation of visible and invisible blocks
    3. Caching of visible blocks
    4. Periodic healing system updates
    5. Batched rendering
    """

    def __init__(self):
        # Множество блоков, которые нуждаются в обновлении
        self.dirty_blocks: Set[Block] = set()

        # Блоки, которые были повреждены и могут лечиться
        self.healing_blocks: Set[Block] = set()

        # Кеш видимых блоков для текущего кадра
        self.visible_blocks_cache: List[Block] = []
        self.cache_valid = False
        self.last_camera_y = None

        # Счетчик кадров для периодических обновлений
        self.frame_counter = 0

        # Блоки, сгруппированные по типу для пакетного рендеринга
        self.render_batches: Dict[str, List[Tuple[Block, Tuple[int, int]]]] = {}

        # Последний раз когда проверяли лечение
        self.last_healing_check = 0
        self.healing_check_interval = 1000  # Проверяем лечение раз в секунду

    def mark_block_dirty(self, block: Block):
        """Отметить блок как нуждающийся в обновлении"""
        self.dirty_blocks.add(block)

        # Если блок поврежден, добавляем в систему лечения
        if block.hp < block.max_hp and not block.destroyed:
            self.healing_blocks.add(block)

    def get_visible_blocks(self, camera_y: float, start_chunk_y: int, end_chunk_y: int,
                          get_block_func) -> List[Block]:
        """
        Get visible blocks based on camera position and chunk range.
        """
        # Проверяем, нужно ли обновить кеш
        if (not self.cache_valid or
            self.last_camera_y is None or
            abs(camera_y - self.last_camera_y) > BLOCK_SIZE * 2):

            self.visible_blocks_cache.clear()
            self.last_camera_y = camera_y

            # Собираем все видимые блоки
            for chunk_x in range(-1, 2):
                for chunk_y in range(start_chunk_y, end_chunk_y):
                    for y in range(CHUNK_HEIGHT):
                        for x in range(CHUNK_WIDTH):
                            block = get_block_func(chunk_x, chunk_y, x, y)
                            if block is not None and not block.destroyed:
                                self.visible_blocks_cache.append(block)

            self.cache_valid = True

        return self.visible_blocks_cache

    def update_blocks_optimized(self, space, hud, camera_y: float, start_chunk_y: int,
                               end_chunk_y: int, get_block_func):
        """
        Update blocks with optimizations
        """
        self.frame_counter += 1
        current_time = pygame.time.get_ticks()

        # Получаем видимые блоки
        visible_blocks = self.get_visible_blocks(camera_y, start_chunk_y, end_chunk_y, get_block_func)

        # 1. Обновляем только "грязные" блоки каждый кадр
        dirty_blocks_copy = self.dirty_blocks.copy()
        for block in dirty_blocks_copy:
            if block.destroyed:
                self.dirty_blocks.discard(block)
                self.healing_blocks.discard(block)
                continue

            # Обновляем блок
            self._update_single_block(block, space, hud)

            # Если блок больше не нуждается в постоянных обновлениях, убираем из dirty
            if block.hp == block.max_hp and block.first_hit_time is None:
                self.dirty_blocks.discard(block)


    def _update_single_block(self, block: Block, space, hud):
        """Обновить один блок"""
        # Проверяем только если блок был поврежден
        if block.first_hit_time is None and block.hp < block.max_hp:
            block.first_hit_time = pygame.time.get_ticks()
            block.last_heal_time = block.first_hit_time

        # Проверяем уничтожение
        if block.hp <= 0 and not block.destroyed:
            block.destroyed = True
            space.remove(block.body, block.shape)

            # Добавляем ресурсы в HUD
            self._add_block_resources(block, hud)

            # Убираем из всех списков
            self.dirty_blocks.discard(block)
            self.healing_blocks.discard(block)
            self.cache_valid = False  # Инвалидируем кеш

    def _add_block_resources(self, block: Block, hud):
        """Add resources to HUD based on block type."""
        import random

        resource_map = {
            "coal_ore": ("coal", 1),
            "iron_ore": ("iron_ingot", 1),
            "copper_ore": ("copper_ingot", 1),
            "gold_ore": ("gold_ingot", 1),
            "diamond_ore": ("diamond", 1),
            "emerald_ore": ("emerald", 1),
            "redstone_ore": ("redstone", random.randint(4, 5)),
            "lapis_ore": ("lapis_lazuli", random.randint(4, 8))
        }

        if block.name in resource_map:
            resource_name, amount = resource_map[block.name]
            hud.amounts[resource_name] += amount

    def prepare_render_batches(self, visible_blocks: List[Block], camera) -> Dict[str, List[Tuple[Block, Tuple[int, int]]]]:
        """
        Prepare render batches for visible blocks to optimize rendering.
        """
        self.render_batches.clear()

        for block in visible_blocks:
            if block.destroyed:
                continue

            # Вычисляем позицию блока на экране
            block_x = block.body.position.x - camera.offset_x - BLOCK_SIZE // 2
            block_y = block.body.position.y - camera.offset_y - BLOCK_SIZE // 2

            position = (int(block_x), int(block_y))

            # Группируем по типу блока
            if block.name not in self.render_batches:
                self.render_batches[block.name] = []

            self.render_batches[block.name].append((block, position))

        return self.render_batches

    def draw_blocks_batched(self, screen, visible_blocks: List[Block], camera):
        """
        Draw visible blocks using batched rendering for performance.
        """
        # Подготавливаем пакеты
        batches = self.prepare_render_batches(visible_blocks, camera)

        # Рендерим каждый тип блоков пакетом
        for _, block_data in batches.items():
            # Сначала рендерим основные текстуры блоков
            blits_data = []
            for block, position in block_data:
                blits_data.append((block.texture, position))

            if blits_data:
                screen.blits(blits_data)

            # Затем рендерим overlay повреждений для поврежденных блоков
            damage_blits = []
            for block, position in block_data:
                if block.hp < block.max_hp:
                    damage_stage = int((1 - (block.hp / block.max_hp)) * 9)
                    damage_stage = min(damage_stage, 9)

                    destroy_texture = block.texture_atlas.subsurface(
                        block.atlas_items["destroy_stage"][f"destroy_stage_{damage_stage}"]
                    )
                    damage_blits.append((destroy_texture, position))

            if damage_blits:
                screen.blits(damage_blits)

    def invalidate_cache(self):
        """Invalidate the visible blocks cache."""
        self.cache_valid = False

    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the block manager's performance."""
        return {
            "dirty_blocks": len(self.dirty_blocks),
            "healing_blocks": len(self.healing_blocks),
            "cached_visible": len(self.visible_blocks_cache),
            "cache_valid": self.cache_valid,
            "frame_counter": self.frame_counter
        }
