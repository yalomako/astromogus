import pygame as pg

pg.init()

class BaseTask(pg.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.complete = False
        self.started = False
        self.complete_sound = pg.mixer.Sound('../sounds/task_completed.mp3')
        self.def_font = pg.font.SysFont("arial", 30, True)
        self.moving_sprites = pg.sprite.Group()
        self.press_f_image = self.def_font.render('Нажмите F', True, 'black')
