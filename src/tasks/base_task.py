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


class Checkpoint(pg.sprite.Sprite):
    def __init__(self, size: tuple, pos: tuple, *groups):
        super().__init__(*groups)
        self.image = pg.Surface(size)
        self.image.fill("green")
        self.image.set_alpha(0)

        self.rect = self.image.get_rect(center=pos)

        self.transparency = 0
        self.switch = False

    def animate(self):
        self.transparency += 2
        self.image.set_alpha(self.transparency)
        if self.transparency >= 100:
            self.transparency = 0

    def activate(self):
        if not self.switch:
            self.switch = True

    def update(self):
        if self.switch:
            self.animate()
