import pygame as pg
from charecters import Player
from map import Camera, Room
from support import rooms_info
from tasks.task1 import TaskVirus
from tasks.task2 import TaskTubes
from tasks.task3 import AsteroidTask

pg.init()


class Game:
    main_theme = pg.mixer.Sound('sounds/soundtrack1.mp3')
    main_theme.set_volume(0.25)
    pg.display.set_caption('Astromogus')
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
        self.task2 = TaskTubes()
        self.task3 = AsteroidTask()
        self.camera_group.add(*self.task1.moving_sprites)
        # Player
        self.player = Player(self.camera_group)

    def run(self):
        self.main_theme.play(-1)
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
            self.screen.fill('black')
            #______исправить______
            if self.task1.complete and not self.task2.started:
                self.camera_group.remove(*self.task1.moving_sprites)
                self.camera_group.add(*self.task2.moving_sprites)
                self.static_group.add(self.task2)
                self.task2.started = True
            elif self.task2.complete and not self.task3.started:
                self.camera_group.remove(*self.task2.moving_sprites)
                self.camera_group.add(*self.task3.moving_sprites)
                self.static_group.add(self.task3)
                self.task3.started = True
            #_____________________________________________________
            self.camera_group.custom_draw(self.player)
            self.camera_group.update()
            self.static_group.update(self.player)

            pg.display.update()
            self.fr.tick(60)


game = Game()
game.run()
