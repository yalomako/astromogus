import pygame as pg
from support import get_hitboxes

class Room(pg.sprite.Sprite):
    ALL_HIT_BOXES = []

    def __init__(self, group, image_path: str, pos: tuple, style: str):
        super().__init__(group)
        self.image = pg.image.load(image_path)
        self.rect = self.image.get_rect(topleft=pos)

        self.hit_boxes = get_hitboxes(pos, style)
        Room.add_hit_boxes(self.hit_boxes)

    @classmethod
    def add_hit_boxes(cls, hit_boxes):
        cls.ALL_HIT_BOXES.extend(hit_boxes)

    def update(self):
        pass
        # for hit_box in self.ALL_HIT_BOXES:
        #     pg.draw.rect(pg.display.get_surface(), 'red', hit_box, 2)



class Camera(pg.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pg.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2

        self.offset = pg.math.Vector2()

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def custom_draw(self, player):
        self.center_target_camera(player)
        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)