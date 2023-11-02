import pygame as pg
import random as rd
import time
from base_task import *
from task1 import Checkpoint
class Asteroid(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.image.load('images/asteroid_image.png')
        self.rect = self.image.get_rect(midleft=(125, rd.randint(150, 625)))
        self.image = pg.image.load('../images/asteroid_image.png')
        self.rect = self.image.get_rect(midleft=(rd.randint(103, 560), rd.randint(103, 561)))
        self.clicked = False
        self.killed = False
        self.boom_images = [pg.image.load(f'images/aster_boom{i}.png')for i in range(1,4)]
        self.animation_timer = 0
        self.dir = self.get_dir()

    def destroy(self):
         self.animation_timer += 1
         if self.animation_timer == 21:
             self.kill()
         if self.animation_timer in (0, 10, 20):
            self.image = self.boom_images[self.animation_timer // 10]

    def get_dir(self):
        start_dir = pg.Vector2()
        if self.rect.centerx >= 375 and self.rect.centery >= 375:
            start_dir.x = rd.randint(-3, -1)
            start_dir.y = rd.randint(-3, -1)
        elif self.rect.centerx <= 375 and self.rect.centery <= 375:
            start_dir.x = rd.randint(1, 3)
            start_dir.y = rd.randint(1, 3)
        elif self.rect.centerx <= 375 and self.rect.centery >= 375:
            start_dir.x = rd.randint(1, 3)
            start_dir.y = rd.randint(-3, -1)
        else:
            start_dir.x = rd.randint(-3, -1)
            start_dir.y = rd.randint(1, 3)
        return start_dir
    def move(self):
        self.rect.center += self.dir
        if self.rect.right >= 650 or self.rect.left <= 101 or self.rect.bottom >= 650 or self.rect.top <= 101:
            self.kill()
    def update(self):
        pg.display.get_surface().blit(self.image, self.rect)
        self.move()


class Counter():
    def __init__(self):
        self.font = pg.font.SysFont("arial", 30, True)
        self.image = self.font.render('0', False, 'black')
        self.rect = self.image.get_rect(topleft = (100, 100))
        self.number = 0
    def count(self):
        self.number += 1
        self.image = self.font.render(self.number.__str__(), False, 'black')

    def update(self):
        pg.display.get_surface().blit(self.image, self.rect)

class Aim():
    def __init__(self):
        self.image = pg.image.load('images/aim_image.png')
        self.rect = self.image.get_rect(center=(325, 325))
        self.shooting = False
    def shoot_scope(self):
        mouse_pos = pg.mouse.get_pos()
        if pg.mouse.get_pressed()[0]:
            if mouse_pos[1] in range(119, 631):
                self.rect.centery = mouse_pos[1]
            if mouse_pos[0] in range(119, 631):
                self.rect.centerx = mouse_pos[0]
            self.shooting = True
        else:
                self.shooting = False
    def draw_lines(self):
        pg.draw.line(pg.display.get_surface(), 'black', (100, 650), self.rect.center, 5)
        pg.draw.line(pg.display.get_surface(), 'black', (650, 650), self.rect.center, 5)
    def update(self):
        pg.display.get_surface().blit(self.image, self.rect)
        self.draw_lines()
        self.shoot_scope()

class AsteroidInterface():
   def __init__(self):
      super().__init__()
      self.image = pg.Surface((550, 550))
      self.rect = self.image.get_rect(topleft = (100, 100))
      self.image.fill('white')
      self.finished = False
      self.timer = 0
      self.aim = Aim()
      self.fps = pg.time.Clock()
      self.counter = Counter()
      self.asteroids = pg.sprite.Group(
        Asteroid()
      )

   def update(self):
        flag = True
        while flag:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    flag = False
            pg.display.get_surface().blit(self.image, self.rect)
            self.timer += 1
            if self.timer >= 60:
                self.timer = 0
                self.asteroids.add(Asteroid())
            for i in self.asteroids:
                if self.aim.shooting and i.rect.collidepoint(pg.mouse.get_pos()):
                    i.destroy()
                    if i not in self.asteroids:
                        self.counter.count()
            if self.counter.number == 10:
                self.finished = True
                flag = False
            self.asteroids.update()
            self.counter.update()
            self.aim.update()
            self.fps.tick(60)
            pg.display.update()



class AsteroidTask(BaseTask):
    def __init__(self):
        super().__init__()
        self.image = self.def_font.render("Задание Asteroid[-]", True, "White", "Black")
        self.rect = self.image.get_rect()
        self.checkpoint = Checkpoint((50, 50), (1200, -250))
        self.checkpoint.activate()
        self.moving_sprites.add(self.checkpoint)
        self.interface = AsteroidInterface()

    def open_interface(self, pla):
        f_key_pressed = pg.key.get_pressed()[pg.K_f]
        if self.checkpoint.rect.colliderect(pla.rect):
            pg.display.get_surface().blit(self.press_f_image, (300, 400))
            if f_key_pressed:
                self.interface.update()

    def update(self, pl):
        pg.display.get_surface().blit(self.image, self.rect)
        self.checkpoint.update()
        self.open_interface(pl)

