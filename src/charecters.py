import pygame as pg
from support import walk_images
from task1 import Virus
from map import Room


class Player(pg.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.default_image = pg.transform.scale(pg.image.load("images/pl/idle.png"), (50, 63))
        self.image = self.default_image
        self.walk_images = walk_images

        self.rect = self.image.get_rect(center=(pg.display.get_window_size()[0] // 2,
                                                pg.display.get_window_size()[1] // 2))

        self.speed = 3
        self.direction = pg.math.Vector2()

        self.animation_timer = 0

    def set_dir(self):
        keys = pg.key.get_pressed()

        if keys[pg.K_a]:
            self.direction.x = -1
        elif keys[pg.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

        if keys[pg.K_s]:
            self.direction.y = 1
        elif keys[pg.K_w]:
            self.direction.y = -1
        else:
            self.direction.y = 0

    def colliding_x(self, hit_boxes: list):
        for hit_box in hit_boxes:
            if self.rect.colliderect(hit_box):
                if self.direction.x == -1:
                    self.rect.left += self.speed
                elif self.direction.x == 1:
                    self.rect.right -= self.speed

    def colliding_y(self, hit_boxes: list):
        for hit_box in hit_boxes:
            if self.rect.colliderect(hit_box):
                if self.direction.y == -1:
                    self.rect.top += self.speed
                elif self.direction.y == 1:
                    self.rect.bottom -= self.speed

    def move(self):
        self.rect.centerx += self.direction.x * self.speed
        self.colliding_x(Room.ALL_HIT_BOXES)
        self.rect.centery += self.direction.y * self.speed
        self.colliding_y(Room.ALL_HIT_BOXES)

    def animate(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_d] or keys[pg.K_a] or keys[pg.K_s] or keys[pg.K_w]:
            self.animation_timer += 1
            if self.animation_timer == 60:
                self.animation_timer = 0
            if (keys[pg.K_d] or keys[pg.K_s]) and not keys[pg.K_a]:
                self.image = self.walk_images[self.animation_timer // 5]
            elif keys[pg.K_a] or keys[pg.K_w]:
                self.image = pg.transform.flip(self.walk_images[self.animation_timer // 5], True, False)
        else:
            if self.direction == 1:
                self.image = self.default_image
            else:
                self.image = pg.transform.flip(self.default_image, True, False)

    def take(self, bruh):
        keys = pg.key.get_pressed()
        for i in bruh:
            if self.rect.colliderect(i.rect) and keys[pg.K_c]:
                if isinstance(i, Virus):
                    i.kill()

    def update(self):
        self.set_dir()
        self.move()
        self.animate()
