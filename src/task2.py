import pygame as pg
from base_task import *
from task1 import Checkpoint

class Tube(pg.sprite.Sprite):
   def __init__(self, pos, color, id: int, side):
      super().__init__()
      self.image = pg.Surface((25, 50))
      self.rect = self.image.get_rect(topleft = pos)
      self.image.fill(color)
      self.id = id
      self.side = side
      self.busy = False
      self.color = color
      self.pos = pos
   def is_chosen(self):
      mouse_pos = pg.mouse.get_pos()
      mouse_clicked = pg.mouse.get_pressed()[0]
      if self.rect.collidepoint(mouse_pos) and mouse_clicked:
         return True


   def update(self, surface):
      surface.blit(self.image, self.rect)
class TubesInterface(pg.sprite.Sprite):
   def __init__(self):
      super().__init__()
      self.image = pg.Surface((550, 550))
      self.rect = self.image.get_rect(topleft = (100, 100))
      self.first_chosen = None
      self.second_chosen = None
      self.tubes = pg.sprite.Group(
         Tube((0 + self.rect.x, 110 + self.rect.y), "yellow", 1, 1),
         Tube((0 + self.rect.x, 220 + self.rect.y), "green", 2, 1),
         Tube((0 + self.rect.x, 330 + self.rect.y), "blue", 3, 1),
         Tube((0 + self.rect.x, 440 + self.rect.y), "orange", 4, 1),
         Tube((525+ self.rect.x, 110 + self.rect.y), "green", 2, 2),
         Tube((525 + self.rect.x, 220 + self.rect.y), "orange", 4, 2),
         Tube((525 + self.rect.x, 330 + self.rect.y), "yellow", 1, 2),
         Tube((525 + self.rect.x, 440 + self.rect.y), "blue", 3, 2)
      )
      self.completed_tubes = []
      self.image.fill("white")
      self.mark = pg.image.load("images/check_mark.png")
      self.finished = False
   def check_tubes(self):
      for i in self.tubes:
         if i.is_chosen():
            if self.first_chosen == None and i.side == 1:
                  self.first_chosen = i
            elif self.second_chosen == None and i.side == 2:
               self.second_chosen = i
   def check_connection(self):
      if self.first_chosen and self.second_chosen:
         if self.first_chosen.id == self.second_chosen.id and not self.first_chosen.busy and not self.second_chosen.busy:
            self.completed_tubes.append((self.first_chosen, self.second_chosen))
            self.first_chosen.busy = True
            self.second_chosen.busy = True
         self.first_chosen = None
         self.second_chosen = None
   def complete(self):
      if len(self.completed_tubes) == 4:
         pg.display.get_surface().blit(self.mark, (225, 100))
         self.finished = True

   def draw_lines(self):
      for i in self.completed_tubes:
         pg.draw.line(pg.display.get_surface(), i[0].color, i[0].rect.center, i[1].rect.center, 25)
   def animate(self):
      if self.first_chosen:
         pg.draw.rect(pg.display.get_surface(), "red", self.first_chosen.rect, 2)
      if self.second_chosen:
         pg.draw.rect(pg.display.get_surface(), "red", self.second_chosen.rect, 2)
   def update(self):
      flag = True
      while flag:
         for event in pg.event.get():
            if event.type == pg.QUIT:
               exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
               flag = False
         self.check_tubes()
         self.check_connection()
         pg.display.get_surface().blit(self.image, self.rect)
         self.tubes.update(pg.display.get_surface())
         self.draw_lines()
         self.animate()
         self.complete()
         pg.display.update()

class Tap():
   def __init__(self, pos):
      self.image = pg.Surface((50, 50))
      self.rect = self.image.get_rect(topleft = pos)


class WaterInterface(pg.sprite.Sprite):
   def __init__(self, pos):
      super().__init__()
      self.image = pg.Surface((550, 550))
      self.rect = self.image.get_rect(topleft = (100, 100))

   def update(self):
      flag = True
      while flag:
         for event in pg.event.get():
            if event.type == pg.QUIT:
               exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
               flag = False
         pg.display.get_surface().blit(self.image, self.rect)
         pg.display.update()



class TaskTubes(BaseTask):
   def __init__(self, *groups):
      super().__init__(*groups)
      self.image = self.def_font.render("Задание tubes[-]", True, "White", "Black")
      self.rect = self.image.get_rect(y = 50)

      self.interface = TubesInterface()
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
      if not self.interface.finished:
         self.open_interface(player)
      else:
         self.checkpoint.switch = False
         self.checkpoint = Checkpoint((50, 100), (0, 0), self.moving_sprites)
         self.checkpoint.activate()
