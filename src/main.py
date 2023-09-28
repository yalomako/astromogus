import pygame as pg
from charecters import Player
from map import Camera, Room
from support import rooms_info
from src.task1 import TaskVirus
from task2 import TaskTubes
pg.init()

class Game:
    soundtrack1 = pg.mixer.Sound('sounds/soundtrack1.mp3')
    walking = pg.mixer.Sound('sounds/walking.mp3')
    open_interface = pg.mixer.Sound('sounds/open_interface.mp3')
    def __init__(self):
        self.screen = pg.display.set_mode((700, 700))
        self.fr = pg.time.Clock()


        # Main groups
        self.camera_group = Camera()
        self.static_group = pg.sprite.Group()

        # Rooms
        self.rooms = [Room(self.camera_group, *info) for info in rooms_info]

        # Tasks
        self.task1 = TaskVirus(self.static_group)
        self.task2 = TaskTubes(self.open_interface)
        self.camera_group.add(*self.task1.moving_sprites)
        # Player
        self.player = Player(self.camera_group, self.walking)

    def run(self):
        self.soundtrack1.play(-1)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            self.screen.fill('black')
            if self.task1.complete and not self.task2.started:
                self.camera_group.remove(*self.task1.moving_sprites)
                self.camera_group.add(*self.task2.moving_sprites)
                self.static_group.add(self.task2)
                self.task2.started = True
            self.camera_group.custom_draw(self.player)
            self.camera_group.update()
            self.static_group.update(self.player)

            pg.display.update()
            self.fr.tick(60)


game = Game()
game.run()
