import numpy as np
import pygame as pg
from settings import *
from chess_piece import *
from widgets import Widget, ColorPickWidget, rgb_color1pick_image, rgb_color2pick_image, rgb_color3pick_image

standard_position_map = (
    ('br', 'bn', 'bb', 'bq', 'bk', 'bb', 'bn', 'br'),
    ('bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'),
    ('__', '__', '__', '__', '__', '__', '__', '__'),
    ('__', '__', '__', '__', '__', '__', '__', '__'),
    ('__', '__', '__', '__', '__', '__', '__', '__'),
    ('__', '__', '__', '__', '__', '__', '__', '__'),
    ('wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'),
    ('wr', 'wn', 'wb', 'wq', 'wk', 'wb', 'wn', 'wr')
)


class Map:
    def __init__(self, game, position_map=standard_position_map):
        self.game = game
        self.updated_map = position_map
        self.image = pg.image.load('ressources/chessboard_image.png')
        self.image = pg.transform.scale(self.image, RES)
        self.board = [[pg.Rect(x * SCALED_COORD, y * SCALED_COORD, SCALED_COORD, SCALED_COORD) for x in range(8)]
                      for y in range(8)]
        self.color1 = (200, 173, 128)
        self.color2 = (100, 73, 28)
        self.color3 = (100, 50, 0)
        self.set_pieces_on_board()
        self.is_indicationing = False
        self.arrows_coord = []
        self.squares_coord = []
        self.indication_start_xy = self.indication_start_x, self.indication_start_y = 0, 0
        self.indication_end_xy = self.indication_end_x, self.indication_end_y = 0, 0
        self.subsurface = pg.Surface(RES, pg.SRCALPHA)
        ColorPickWidget(self.game, [520, 30], width=127, height=127,
                        image=rgb_color1pick_image,
                        func=self.change_board_color1)
        ColorPickWidget(self.game, [520, 200], width=127, height=127,
                        image=rgb_color2pick_image,
                        func=self.change_board_color2)
        ColorPickWidget(self.game, [520, 370], width=127, height=127,
                        image=rgb_color3pick_image,
                        func=self.change_square_color)

    def set_pieces_on_board(self):
        for y in range(8):
            for x in range(8):
                match self.updated_map[y][x][1]:
                    case 'q':
                        chess_pieces[y][x] = Queen(self.game, [x, y], self.updated_map[y][x][0])
                    case 'r':
                        chess_pieces[y][x] = Rook(self.game, [x, y], self.updated_map[y][x][0])
                    case 'b':
                        chess_pieces[y][x] = Bishop(self.game, [x, y], self.updated_map[y][x][0])
                    case 'n':
                        chess_pieces[y][x] = Knight(self.game, [x, y], self.updated_map[y][x][0])
                    case 'p':
                        chess_pieces[y][x] = Pawn(self.game, [x, y], self.updated_map[y][x][0])
                    case 'k':
                        chess_pieces[y][x] = King(self.game, [x, y], self.updated_map[y][x][0])

    def change_board_color1(self):
        x, y = pg.mouse.get_pos()[0] - 520, pg.mouse.get_pos()[1] - 30
        x, y = x / 127, y / 127
        self.color1 = get_color(x, y, *rgb_square_points)
        self.color1 = (255 - self.color1[0], 255 - self.color1[1], 255 - self.color1[2])
        return self.color1

    def change_board_color2(self):
        x, y = pg.mouse.get_pos()[0] - 520, pg.mouse.get_pos()[1] - 200
        x, y = x / 127, y / 127
        self.color2 = get_color(x, y, *rgb_square_points)
        self.color2 = (255 - self.color2[0], self.color2[1], self.color2[2])
        return self.color2

    def change_square_color(self):
        x, y = pg.mouse.get_pos()[0] - 520, pg.mouse.get_pos()[1] - 370
        x, y = x / 127, y / 127
        self.color3 = get_color(x, y, *rgb_square_points)
        self.color3 = (255 - self.color3[0], 255 - self.color3[1], 255 - self.color3[2])
        return self.color3

    def check_start_indicationing(self):
        x = pg.mouse.get_pos()[0] * 8 // WIDTH * SCALED_COORD + SCALED_COORD // 2
        y = pg.mouse.get_pos()[1] * 8 // WIDTH * SCALED_COORD + SCALED_COORD // 2
        mouse_state = pg.mouse.get_pressed()
        if not mouse_state[2]:
            self.is_indicationing = False
        elif not self.is_indicationing:
            self.is_indicationing = True
            self.indication_start_xy = self.indication_start_x, self.indication_start_y = x, y

    def check_end_indicationing(self):
        mouse_state = pg.mouse.get_pressed()
        if self.is_indicationing and not mouse_state[2]:
            x = pg.mouse.get_pos()[0] * 8 // WIDTH * SCALED_COORD
            y = pg.mouse.get_pos()[1] * 8 // WIDTH * SCALED_COORD
            self.indication_end_xy = self.indication_end_x, self.indication_end_y = x + SCALED_COORD // 2, y + SCALED_COORD // 2
            if self.indication_start_xy != self.indication_end_xy:
                if (self.indication_start_xy, self.indication_end_xy) not in self.arrows_coord:
                    self.arrows_coord.append((self.indication_start_xy, self.indication_end_xy))
                else:
                    self.arrows_coord.remove((self.indication_start_xy, self.indication_end_xy))
            elif (x, y) not in self.squares_coord:
                self.squares_coord.append((x, y))
            else:
                self.squares_coord.remove((x, y))

    def check_erase_indications(self):
        if pg.mouse.get_pressed()[0] and pg.mouse.get_pos()[0] < 500 and pg.mouse.get_pos()[1] < 500:
            self.arrows_coord.clear()
            self.squares_coord.clear()

    def indication_update(self):
        self.check_erase_indications()
        self.check_end_indicationing()
        self.check_start_indicationing()

    def chess_pieces_update(self):
        for y in chess_pieces:
            for i in y:
                if i:
                    i.update()

    def update(self):
        self.image = pg.image.load('ressources/chessboard_image.png')
        self.image = pg.transform.scale(self.image, RES)
        self.chess_pieces_update()
        self.indication_update()

    def draw(self):
        for y, j in enumerate(self.board):
            for x, i in enumerate(j):
                color = self.color2 if (x + y) % 2 else self.color1
                pg.draw.rect(self.game.screen, color, i)
        #        self.game.screen.blit(self.image, (0, 0))
        idk_anymore = []
        for y in chess_pieces:
            for i in y:
                if i:
                    if i.priority < 3:
                        idk_anymore.append(i)
                    else:
                        i.draw(self.color3)
        for i in idk_anymore:
            i.draw(self.color3)
        self.subsurface = pg.Surface(RES, pg.SRCALPHA)
        for i in self.squares_coord:
            pg.draw.rect(self.subsurface, (*self.color3, 128), (i[0], i[1], SCALED_COORD, SCALED_COORD))
        for i in self.arrows_coord:
            pg.draw.line(self.subsurface, (0, 0, 0, 128), i[0], (i[1][0], i[1][1]), 6)
            pg.draw.circle(self.subsurface, (100, 0, 0, 125), i[1], 10)
        self.game.screen.blit(self.subsurface, [0, 0])
