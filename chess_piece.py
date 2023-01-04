import pygame as pg
from settings import *

_ = False

dict_of_chess_pieces_image = {
    'w': {'b': 'ressources/white_bishop.png',
          'k': 'ressources/white_king.png',
          'n': 'ressources/white_knight.png',
          'p': 'ressources/white_pawn.png',
          'q': 'ressources/white_queen.png',
          'r': 'ressources/white_rook.png'},
    'b': {'b': 'ressources/black_bishop.png',
          'k': 'ressources/black_king.png',
          'n': 'ressources/black_knight.png',
          'p': 'ressources/black_pawn.png',
          'q': 'ressources/black_queen.png',
          'r': 'ressources/black_rook.png'}
}
all_moves_w = []
all_moves_b = []


class TurnKeeper:
    def __init__(self, s: str):
        self.turn = s if s in 'wb' else 'w'

    def change_turn(self):
        self.turn = 'w' if self.turn == 'b' else 'b'
        global all_moves_w, all_moves_b
        all_moves_w = all_moves_b = []


turn_keeper = TurnKeeper(FIRST_TURN)


class Queen:

    def __init__(self, game, xy: list[int, int], color: str = 'w', name: str = 'q'):
        self.game = game
        self.xy = self.x, self.y = xy
        self.color = color
        self.name = name
        self.image = pg.image.load(dict_of_chess_pieces_image[color][name]).convert_alpha()
        self.image = pg.transform.scale(self.image, (SCALED_COORD, SCALED_COORD))
        self.hitbox = self.image.get_rect()
        self.half_width = self.image.get_width() // 2
        self.half_height = self.image.get_height() // 2
        self.is_dragging = False
        self.previous_mouse_state = pg.mouse.get_pressed()
        self.moves_allowed = []
        self.priority = 3
        self.subsurface = pg.Surface(RES, pg.SRCALPHA)

    def is_hold(self):
        mouse_state = pg.mouse.get_pressed()
        if not mouse_state[0]:
            self.is_dragging = False
        elif self.hitbox.collidepoint(pg.mouse.get_pos()):
            if mouse_state != self.previous_mouse_state:
                self.is_dragging = True
                self.priority = 1
        self.previous_mouse_state = mouse_state

    def move(self, _x, _y):
        x, y = _x * 8 // WIDTH, _y * 8 // WIDTH
        if (x, y) in self.moves_allowed:
            chess_pieces[self.y][self.x] = _
            chess_pieces[y][x] = self
            self.xy = self.x, self.y = [x, y]
            turn_keeper.change_turn()

    def check_moves(self, pos):

        moves = []
        # horizontal and vertical
        # ->
        for x in range(pos[0] + 1, 8, 1):
            if isinstance(chess_pieces[pos[1]][x], bool):
                moves.append((x, pos[1]))
            elif self.color != chess_pieces[pos[1]][x].color:
                moves.append((x, pos[1]))
                break
            else:
                break

        # <-
        for x in range(pos[0] - 1, -1, -1):
            if isinstance(chess_pieces[pos[1]][x], bool):
                moves.append((x, pos[1]))
            elif self.color != chess_pieces[pos[1]][x].color:
                moves.append((x, pos[1]))
                break
            else:
                break

        # down
        for y in range(pos[1] + 1, 8, 1):
            if isinstance(chess_pieces[y][pos[0]], bool):
                moves.append((pos[0], y))
            elif self.color != chess_pieces[y][pos[0]].color:
                moves.append((pos[0], y))
                break
            else:
                break

        # up
        for y in range(pos[1] - 1, -1, -1):
            if isinstance(chess_pieces[y][pos[0]], bool):
                moves.append((pos[0], y))
            elif self.color != chess_pieces[y][pos[0]].color:
                moves.append((pos[0], y))
                break
            else:
                break

        # diagonals
        # down right
        for g in range(1, 8, 1):
            if 8 in [pos[0] + g, pos[1] + g]:
                break
            if isinstance(chess_pieces[pos[1] + g][pos[0] + g], bool):
                moves.append((pos[0] + g, pos[1] + g))
            elif self.color != chess_pieces[pos[1] + g][pos[0] + g].color:
                moves.append((pos[0] + g, pos[1] + g))
                break
            else:
                break

        # up left
        for g in range(1, 8, 1):
            if -1 in [pos[0] - g, pos[1] - g]:
                break
            if isinstance(chess_pieces[pos[1] - g][pos[0] - g], bool):
                moves.append((pos[0] - g, pos[1] - g))
            elif self.color != chess_pieces[pos[1] - g][pos[0] - g].color:
                moves.append((pos[0] - g, pos[1] - g))
                break
            else:
                break

        # up right
        for g in range(1, 8, 1):
            if 8 == pos[0] + g or -1 == pos[1] - g:
                break
            if isinstance(chess_pieces[pos[1] - g][pos[0] + g], bool):
                moves.append((pos[0] + g, pos[1] - g))
            elif self.color != chess_pieces[pos[1] - g][pos[0] + g].color:
                moves.append((pos[0] + g, pos[1] - g))
                break
            else:
                break

        # down left
        for g in range(1, 8, 1):
            if -1 == pos[0] - g or 8 == pos[1] + g:
                break
            if isinstance(chess_pieces[pos[1] + g][pos[0] - g], bool):
                moves.append((pos[0] - g, pos[1] + g))
            elif self.color != chess_pieces[pos[1] + g][pos[0] - g].color:
                moves.append((pos[0] - g, pos[1] + g))
                break
            else:
                break

        return moves

    def is_dropped(self):
        if self.is_dragging and not pg.mouse.get_pressed()[0]:
            self.priority = 3
            return True
        else:
            return False

    def check_check(self):
        if self.color == 'w':
            all_moves_w.extend(self.moves_allowed)
        else:
            all_moves_b.extend(self.moves_allowed)

    def draw(self, color):
        if self.is_dragging:
            self.subsurface = pg.Surface((WIDTH, HEIGHT), pg.SRCALPHA)
            for pos in self.moves_allowed:
                pg.draw.circle(self.subsurface, (100, 0, 100, 128),
                               (pos[0] * SCALED_COORD + SCALED_COORD // 2,
                                pos[1] * SCALED_COORD + SCALED_COORD // 2),
                               SCALED_COORD // 2 - 20)
            pg.draw.rect(self.subsurface, (*color, 128), (self.x * SCALED_COORD,
                                                          self.y * SCALED_COORD,
                                                          SCALED_COORD,
                                                          SCALED_COORD))
            self.game.screen.blit(self.subsurface, [0, 0])
            mouse_pos = pg.mouse.get_pos()
            pos = mouse_pos[0] - self.half_width, mouse_pos[1] - self.half_height
            self.game.screen.blit(self.image, pos)
        else:
            self.game.screen.blit(self.image, [self.xy[0] * SCALED_COORD, self.xy[1] * SCALED_COORD])
        self.hitbox.topleft = self.xy[0] * SCALED_COORD, self.xy[1] * SCALED_COORD

    def update(self):
        if turn_keeper.turn == self.color:
            self.moves_allowed = self.check_moves(self.xy)
            if self.is_dropped():
                self.move(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
            self.is_hold()


class Rook(Queen):
    def __init__(self, game, xy: list[int, int], color: str = 'w', name: str = 'r'):
        super().__init__(game, xy, color, name)

    def check_moves(self, pos):
        moves = []

        # horizontal and vertical
        # ->
        for x in range(pos[0] + 1, 8, 1):
            if isinstance(chess_pieces[pos[1]][x], bool):
                moves.append((x, pos[1]))
            elif self.color != chess_pieces[pos[1]][x].color:
                moves.append((x, pos[1]))
                break
            else:
                break

        # <-
        for x in range(pos[0] - 1, -1, -1):
            if isinstance(chess_pieces[pos[1]][x], bool):
                moves.append((x, pos[1]))
            elif self.color != chess_pieces[pos[1]][x].color:
                moves.append((x, pos[1]))
                break
            else:
                break

        # down
        for y in range(pos[1] + 1, 8, 1):
            if isinstance(chess_pieces[y][pos[0]], bool):
                moves.append((pos[0], y))
            elif self.color != chess_pieces[y][pos[0]].color:
                moves.append((pos[0], y))
                break
            else:
                break

        # up
        for y in range(pos[1] - 1, -1, -1):
            if isinstance(chess_pieces[y][pos[0]], bool):
                moves.append((pos[0], y))
            elif self.color != chess_pieces[y][pos[0]].color:
                moves.append((pos[0], y))
                break
            else:
                break

        return moves


class Bishop(Queen):
    def __init__(self, game, xy: list[int, int], color: str = 'w', name: str = 'b'):
        super().__init__(game, xy, color, name)

    def check_moves(self, pos):
        moves = []

        # diagonals
        # down right
        for g in range(1, 8, 1):
            if 8 in [pos[0] + g, pos[1] + g]:
                break
            if isinstance(chess_pieces[pos[1] + g][pos[0] + g], bool):
                moves.append((pos[0] + g, pos[1] + g))
            elif self.color != chess_pieces[pos[1] + g][pos[0] + g].color:
                moves.append((pos[0] + g, pos[1] + g))
                break
            else:
                break

        # up left
        for g in range(1, 8, 1):
            if -1 in [pos[0] - g, pos[1] - g]:
                break
            if isinstance(chess_pieces[pos[1] - g][pos[0] - g], bool):
                moves.append((pos[0] - g, pos[1] - g))
            elif self.color != chess_pieces[pos[1] - g][pos[0] - g].color:
                moves.append((pos[0] - g, pos[1] - g))
                break
            else:
                break

        # up right
        for g in range(1, 8, 1):
            if 8 == pos[0] + g or -1 == pos[1] - g:
                break
            if isinstance(chess_pieces[pos[1] - g][pos[0] + g], bool):
                moves.append((pos[0] + g, pos[1] - g))
            elif self.color != chess_pieces[pos[1] - g][pos[0] + g].color:
                moves.append((pos[0] + g, pos[1] - g))
                break
            else:
                break

        # down left
        for g in range(1, 8, 1):
            if -1 == pos[0] - g or 8 == pos[1] + g:
                break
            if isinstance(chess_pieces[pos[1] + g][pos[0] - g], bool):
                moves.append((pos[0] - g, pos[1] + g))
            elif self.color != chess_pieces[pos[1] + g][pos[0] - g].color:
                moves.append((pos[0] - g, pos[1] + g))
                break
            else:
                break

        return moves


class Knight(Queen):
    def __init__(self, game, xy: list[int, int], color: str = 'w', name: str = 'n'):
        super().__init__(game, xy, color, name)

    def check_moves(self, pos):
        moves = []

        # goofy knight's moves
        for dy in [-2, 2]:
            for dx in [-1, 1]:
                if pos[0] + dx not in [-1, 8] and pos[1] + dy not in [-2, -1, 8, 9]:
                    if isinstance(chess_pieces[pos[1] + dy][pos[0] + dx], bool):
                        moves.append((pos[0] + dx, pos[1] + dy))
                    elif self.color != chess_pieces[pos[1] + dy][pos[0] + dx].color:
                        moves.append((pos[0] + dx, pos[1] + dy))

        for dx in [-2, 2]:
            for dy in [-1, 1]:
                if pos[0] + dx not in [-2, -1, 8, 9] and pos[1] + dy not in [-1, 8]:
                    if isinstance(chess_pieces[pos[1] + dy][pos[0] + dx], bool):
                        moves.append((pos[0] + dx, pos[1] + dy))
                    elif self.color != chess_pieces[pos[1] + dy][pos[0] + dx].color:
                        moves.append((pos[0] + dx, pos[1] + dy))

        return moves


class Pawn(Queen):
    def __init__(self, game, xy: list[int, int], color: str = 'w', name: str = 'p'):
        super().__init__(game, xy, color, name)
        self.has_moved = False

    def check_moves(self, pos):
        moves = []

        # pawn moves :skull:
        if not self.has_moved:
            dy = -2 if self.color == 'w' else 2
            if isinstance(chess_pieces[pos[1] + dy][pos[0]], bool):
                moves.append((pos[0], pos[1] + dy))
        dy = -1 if self.color == 'w' else 1
        if pos[1] + dy != 8 and pos[1] + dy != -1 :
            if isinstance(chess_pieces[pos[1] + dy][pos[0]], bool):
                moves.append((pos[0], pos[1] + dy))
        if pos[0] - 1 != -1 and pos[1] + dy != -1 and pos[1] + dy != 8:
            if not isinstance(chess_pieces[pos[1] + dy][pos[0] - 1], bool):
                if self.color != chess_pieces[pos[1] + dy][pos[0] - 1].color:
                    moves.append((pos[0] - 1, pos[1] + dy))
        if pos[0] + 1 != 8 and pos[1] + dy != -1 and pos[1] + dy != 8:
            if not isinstance(chess_pieces[pos[1] + dy][pos[0] + 1], bool):
                if self.color != chess_pieces[pos[1] + dy][pos[0] + 1].color:
                    moves.append((pos[0] + 1, pos[1] + dy))

        return moves

#    def check_pawn_promotion(self):
 #       if self.color == 'w' and self.y ==
  #          return True if True else False

    def move(self, _x, _y):
        x, y = _x * 8 // WIDTH, _y * 8 // WIDTH
        if (x, y) in self.moves_allowed:
            chess_pieces[self.y][self.x] = _
            chess_pieces[y][x] = self
            self.xy = self.x, self.y = [x, y]
            if not self.has_moved:
                self.has_moved = True
            turn_keeper.change_turn()


class King(Queen):
    def __init__(self, game, xy: list[int, int], color: str = 'w', name: str = 'k'):
        super().__init__(game, xy, color, name)
        self.has_moved = False

    def long_castle(self, moves: list):
        # for a little bit of fun I didn't specify if the rook had to be of the same color as the king 😈
        if isinstance(chess_pieces[self.y][self.x - 1], bool):
            if isinstance(chess_pieces[self.y][self.x - 2], bool):
                if isinstance(chess_pieces[self.y][self.x - 3], bool):
                    if isinstance(chess_pieces[self.y][self.x - 4], Rook):
                        moves.append((self.x - 2, self.y))

    def get_long_castle(self):
        return self.x - 2, self.y

    def short_castle(self, moves: list):
        # to make it adaptable to vertical castle too you'll need to put an if statement
        # if self.y == rook.y then check all the things you need to check and can castle horizontally
        # if self.x == rook.x then .... vertically
        # also add an attribute to the Rook class -> self.hasmoved = False and then check if rook.hasmoved == True or False
        if isinstance(chess_pieces[self.y][self.x + 1], bool):
            if isinstance(chess_pieces[self.y][self.x + 2], bool):
                if isinstance(chess_pieces[self.y][self.x + 3], Rook):
                    moves.append((self.x + 2, self.y))
        return None

    def get_short_castle(self):
        return self.x + 2, self.y

    def check_moves(self, pos):
        moves = []

        if not self.has_moved:
            self.long_castle(moves)
            self.short_castle(moves)
        y = pos[1] + 1
        x = pos[0] + 1
        _y = pos[1] - 1
        _x = pos[0] - 1
        if y != 8:
            if isinstance(chess_pieces[y][pos[0]], bool):
                moves.append((pos[0], y))
            elif self.color != chess_pieces[y][pos[0]].color:
                moves.append((pos[0], y))
        if x != 8:
            if isinstance(chess_pieces[pos[1]][x], bool):
                moves.append((x, pos[1]))
            elif self.color != chess_pieces[pos[1]][x].color:
                moves.append((x, pos[1]))
        if _y != -1:
            if isinstance(chess_pieces[_y][pos[0]], bool):
                moves.append((pos[0], _y))
            elif self.color != chess_pieces[_y][pos[0]].color:
                moves.append((pos[0], _y))
        if _x != -1:
            if isinstance(chess_pieces[pos[1]][_x], bool):
                moves.append((_x, pos[1]))
            elif self.color != chess_pieces[pos[1]][_x].color:
                moves.append((_x, pos[1]))
        if y != 8 and x != 8:
            if isinstance(chess_pieces[y][x], bool):
                moves.append((x, y))
            elif self.color != chess_pieces[y][x].color:
                moves.append((x, y))
        if _y != -1 and _x != -1:
            if isinstance(chess_pieces[_y][_x], bool):
                moves.append((_x, _y))
            elif self.color != chess_pieces[_y][_x].color:
                moves.append((_x, _y))
        if y != 8 and _x != -1:
            if isinstance(chess_pieces[y][_x], bool):
                moves.append((_x, y))
            elif self.color != chess_pieces[y][_x].color:
                moves.append((_x, y))
        if _y != -1 and x != 8:
            if isinstance(chess_pieces[_y][x], bool):
                moves.append((x, _y))
            elif self.color != chess_pieces[_y][x].color:
                moves.append((x, _y))

        return moves

    def move(self, _x, _y):
        x, y = _x * 8 // WIDTH, _y * 8 // WIDTH
        if (x, y) in self.moves_allowed:
            chess_pieces[self.y][self.x] = _
            chess_pieces[y][x] = self
            if not self.has_moved:
                if (x, y) == self.get_long_castle():
                    chess_pieces[self.y][self.x - 1] = Rook(self.game, [self.x - 1, self.y],
                                                            chess_pieces[self.y][self.x - 4].color)
                    chess_pieces[self.y][self.x - 4] = _
                elif (x, y) == self.get_short_castle():
                    print('short castle !')
                    chess_pieces[self.y][self.x + 1] = Rook(self.game, [self.x + 1, self.y],
                                                            chess_pieces[self.y][self.x + 3].color)
                    chess_pieces[self.y][self.x + 3] = _
                self.has_moved = True
                print(f'{x, y}')
                print(f'{self.get_short_castle()}')
            self.xy = self.x, self.y = [x, y]
            turn_keeper.change_turn()


chess_pieces: list[list[Queen | Rook | Bishop | Knight | Pawn | King | bool]] = [
    [_ for x in range(8)] for y in range(8)]
