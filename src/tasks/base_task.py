import pygame as pg

pg.init()

class BaseTask(pg.sprite.Sprite):

    def_font = pg.font.SysFont("arial", 30, True)
    def __init__(self, title, *groups):
        super().__init__(*groups)
        self.image = self.def_font.render(f"Задание {title}[-]", True, "White", "Black")
        self.complete_image = self.def_font.render(f"Задание {title}[+]", True, "Green", "Black")
        self.complete = False
        self.started = False
        self.open_sound = pg.mixer.Sound('sounds/open_interface.mp3')
        self.complete_sound = pg.mixer.Sound('sounds/task_completed.mp3')
        self.moving_sprites = pg.sprite.Group()
        self.press_f_image = self.def_font.render('Нажмите F', True, 'black')
