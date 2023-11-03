import pygame as pg

walk_images = tuple(pg.transform.scale(pg.image.load(f"images/player/walk_animation/Walk{i}.png"), (50, 63))
                    for i in range(1, 13))

rooms_info = (
    ('images/locations/up_engine.png', (-320, -90), "up_eng"),
    ("images/locations/hall1.png", (65, 13), "com_eng_caf"),
    ("images/locations/com.png", (237, 190), "communication"),
    ("images/locations/cafeteria.png", (780, -350), "cafeteria"),
    ('images/locations/hall2.png', (1195, 610), "bed_hall")
)


def get_hitboxes(pos: tuple, style):
    rooms_rect = {
        "communication": (
            pg.Rect(pos[0], pos[1], 250, 125),
            pg.Rect(pos[0] + 375, pos[1], 65, 100),
            pg.Rect(pos[0], pos[1]+122, 15, 155),
            pg.Rect(pos[0] + 10, pos[1] + 205, 57, 75),
            pg.Rect(pos[0] + 130, pos[1] + 300, 210, 70),
            pg.Rect(pos[0] + 380, pos[1] + 205, 57, 75),
            pg.Rect(pos[0] + 427, pos[1] + 100, 15, 155)
        ),
        "com_eng_caf": (
            pg.Rect(pos[0] + 13, pos[1], 727, 10),
            pg.Rect(pos[0] + 25, pos[1] + 166, 390, 10),
            pg.Rect(pos[0] + 548, pos[1] + 170, 175, 10)
        ),
        "cafeteria": (
            pg.Rect(pos[0] + 191, pos[1] + 10, 530, 66),
            pg.Rect(pos[0] + 15, pos[1] + 160, 17, 205),
            pg.Rect(pos[0] + 15, pos[1] + 533, 20, 200),
            pg.Rect(pos[0] + 228, pos[1] + 934, 198, 22),
            pg.Rect(pos[0] + 550, pos[1] + 934, 198, 22),
            pg.Rect(pos[0] + 955, pos[1] + 533, 20, 200),
            pg.Rect(pos[0] + 955, pos[1] + 245, 17, 140)
        ),
        "up_eng": (
            pg.Rect(pos[0] + 107, pos[1], 293, 40),
            pg.Rect(pos[0] + 400, pos[1] + 3, 10, 115),
            pg.Rect(pos[0] + 397, pos[1] + 270, 11, 178),
            pg.Rect(pos[0], pos[1] + 130, 315, 200)
        ),
        "bed_hall": (
            pg.Rect(pos[0], pos[1], 10, 303),
            pg.Rect(pos[0] + 135, pos[1], 12, 119),
            pg.Rect(pos[0] + 135, pos[1] + 264, 12, 49)
        )
    }
    return rooms_rect[style]
