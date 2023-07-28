import pygame as pg
from base_task import *
from task1 import Checkpoint

class Tube(pg.sprite.Sprite):
   def __init__(self, pos):
      super().__init__()
      self.image = pg.Surface((50, 50))
      self.rect = self.image.get_rect(center = pos)
   def update(self, surface):
      surface.blit(self.image, self.rect)
class Interface(pg.sprite.Sprite):
   def __init__(self):
      super().__init__()
      self.image = pg.Surface((550, 550))
      self.image.fill("white")
      self.rect = self.image.get_rect(topleft = (100, 100))
      self.tubes = pg.sprite.Group(
         Tube((0, 25)),
         Tube((0, 125)),
         Tube((0, 225)),
         Tube((0, 325))
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
         self.tubes.update(self.image)
         pg.display.update()



class TaskTubes(BaseTask):
   def __init__(self, *groups):
      super().__init__(*groups)
      self.image = self.def_font.render("Задание tubes[-]", True, "White", "Black")
      self.rect = self.image.get_rect(y = 50)

      self.interface = Interface()
      self.checkpoint = Checkpoint((65, 150), (640, 230), self.moving_sprites)
      self.checkpoint.activate()
   def open_interface(self, player):
      f_key_pressed = pg.key.get_pressed()[pg.K_f]
      if self.checkpoint.rect.colliderect(player.rect):
         pg.display.get_surface().blit(self.press_f_image, (300, 400))
         if f_key_pressed:
            self.interface.update()
   def update(self, player):
      pg.display.get_surface().blit(self.image, self.rect)
      self.open_interface(player)
