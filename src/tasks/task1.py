import pygame as pg
from src.tasks.base_task import BaseTask


class Virus(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 50))
        self.rect = self.image.get_rect()
        self.image.fill("green")


class TaskVirus(BaseTask):
    def __init__(self, *groups):
        super().__init__('Virus', *groups)
        self.rect = self.image.get_rect()
        self.started = True
        self.virus = Virus(self.moving_sprites)
        self.checkpoint = Checkpoint((160, 160), (1250, 150), self.moving_sprites)

    def take_virus(self, player):
        if self.virus.rect.colliderect(player.rect) and self.virus.groups():
            pg.display.get_surface().blit(self.press_f_image, (300, 400))
            f_key_pressed = pg.key.get_pressed()[pg.K_f]
            if f_key_pressed:
                self.checkpoint.activate()
                self.virus.kill()

    def complete_task(self, player):
        if self.checkpoint.rect.colliderect(player.rect) and self.checkpoint.groups() and self.checkpoint.switch:
            pg.display.get_surface().blit(self.press_f_image, (300, 400))
            f_key_pressed = pg.key.get_pressed()[pg.K_f]
            if f_key_pressed:
                self.image = self.complete_image
                self.checkpoint.kill()
                self.complete = True
                self.complete_sound.play(0)

    def update(self, player):
        self.take_virus(player)
        self.complete_task(player)
        pg.display.get_surface().blit(self.image, self.rect)
