import pygame as pg
from src.tasks.base_task import BaseTask, Checkpoint


class Tube(pg.sprite.Sprite):
    def __init__(self, pos, color, tube_id: int, side):
        super().__init__()
        self.image = pg.Surface((25, 50))
        self.rect = self.image.get_rect(topleft=pos)
        self.image.fill(color)
        self.id = tube_id
        self.side = side
        self.busy = False
        self.color = color

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
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.first_chosen = None
        self.second_chosen = None
        self.tubes = pg.sprite.Group(
            Tube((0 + self.rect.x, 110 + self.rect.y), "yellow", 1, 1),
            Tube((0 + self.rect.x, 220 + self.rect.y), "green", 2, 1),
            Tube((0 + self.rect.x, 330 + self.rect.y), "blue", 3, 1),
            Tube((0 + self.rect.x, 440 + self.rect.y), "orange", 4, 1),
            Tube((525 + self.rect.x, 110 + self.rect.y), "green", 2, 2),
            Tube((525 + self.rect.x, 220 + self.rect.y), "orange", 4, 2),
            Tube((525 + self.rect.x, 330 + self.rect.y), "yellow", 1, 2),
            Tube((525 + self.rect.x, 440 + self.rect.y), "blue", 3, 2)
        )
        self.completed_tubes = []
        self.image.fill("white")
        self.mark = pg.image.load("images/check_mark.png")
        self.finished = False

    def chose_tube(self):
        for i in self.tubes:
            if i.is_chosen() and not i.busy:
                if self.first_chosen is None and i.side == 1:
                    self.first_chosen = i
                elif self.second_chosen is None and i.side == 2:
                    self.second_chosen = i

    def check_connection(self):
        if self.first_chosen and self.second_chosen:
            if self.first_chosen.id == self.second_chosen.id and not (self.first_chosen.busy and self.second_chosen.busy):
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
            self.chose_tube()
            self.check_connection()
            pg.display.get_surface().blit(self.image, self.rect)
            self.tubes.update(pg.display.get_surface())
            self.draw_lines()
            self.animate()
            self.complete()
            pg.display.update()


class Tap(pg.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.color = "red"
        self.rect = pg.draw.circle(pg.display.get_surface(), self.color, pos, 25)
        self.completed = False

    def change_color(self):
        mouse_clicked = pg.mouse.get_pressed()
        mouse_pos = pg.mouse.get_pos()
        if mouse_clicked[0] and self.rect.collidepoint(mouse_pos):
            self.color = "green"
            self.completed = True

    def update(self):
        self.change_color()
        pg.draw.circle(pg.display.get_surface(), self.color, self.rect.center, 25)


class WaterInterface(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pg.Surface((550, 550))
        self.rect = self.image.get_rect(topleft=(100, 100))
        self.finished = False
        self.completed_taps = []
        self.taps = pg.sprite.Group(
            Tap((200, 375)),
            Tap((310, 375)),
            Tap((420, 375)),
            Tap((530, 375))
        )

    def complete_tap(self):
        for i in self.taps:
            if i.completed:
                self.completed_taps.append(i)
                if len(self.completed_taps) == 4:
                    self.finished = True

    def update(self):
        flag = True
        while flag:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    flag = False
            pg.display.get_surface().blit(self.image, self.rect)
            pg.draw.line(pg.display.get_surface(), "white", (100, 375), (650, 375), 25)
            self.complete_tap()
            self.taps.update()
            pg.display.update()


class TaskTubes(BaseTask):
    def __init__(self, *groups):
        super().__init__('Tubes', *groups)
        self.rect = self.image.get_rect(y=50)
        self.first_interface = TubesInterface()
        self.second_interface = WaterInterface()
        self.interface = self.first_interface
        self.first_checkpoint = Checkpoint((65, 150), (640, 230), self.moving_sprites)
        self.second_checkpoint = Checkpoint((50, 100), (-45, -35), self.moving_sprites)
        self.sound_played = False
        self.checkpoint = self.first_checkpoint
        self.checkpoint.activate()

    def open_interface(self, player):
        f_key_pressed = pg.key.get_pressed()[pg.K_f]
        if self.checkpoint.rect.colliderect(player.rect):
            pg.display.get_surface().blit(self.press_f_image, (300, 400))
            if f_key_pressed:
                self.open_sound.play(0)
                self.interface.update()

    def update(self, player):
        pg.display.get_surface().blit(self.image, self.rect)
        if not self.interface.finished:
            self.open_interface(player)
        elif self.interface is self.first_interface:
            self.interface = self.second_interface
            self.checkpoint.kill()
            self.checkpoint = self.second_checkpoint
            self.checkpoint.activate()
        else:
            self.checkpoint.kill()
            self.complete = True
            if not self.sound_played:
                self.sound_played = True
                self.complete_sound.play(0)
            self.image = self.complete_image
