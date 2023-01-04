import sys

from map import *
from widgets import *
from chess_piece import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((RES[0] + 300, RES[1] + 100))
        self.background = pg.image.load('ressources/blue_background.png')
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        self.pawn_promotion = 'q'

    def new_game(self):
        self.chess_map = Map(self)
        set_widgets(self)

    def update(self):
        self.chess_map.update()
        for i in Widget.widget_list:
            i.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption('goofy chess ☠💀☠')

    def draw(self):
        self.screen.blit(self.background, [0, 0])
        self.chess_map.draw()

    def check_events(self):
        event_list = pg.event.get()
        for event in event_list:
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    self.pawn_promotion = 'r'
                if event.key == pg.K_b:
                    self.pawn_promotion = 'b'
                if event.key == pg.K_n:
                    self.pawn_promotion = 'n'
                if event.key == pg.K_q:
                    self.pawn_promotion = 'q'

    def check_results(self):
        result: int = 0
        color: str = ''
        for y in chess_pieces:
            for chess_piece in y:
                if not isinstance(chess_piece, bool):
                    if chess_piece.name == 'k':
                        result += 1
                        color = chess_piece.color
        if result == 1:
            print('white' if color == 'w' else 'black', 'wins !')
            pg.quit()
            sys.exit()

 #       if not all_moves_w or not all_moves_b:
 #           print('stalemate you noob')
 #           pg.quit()
 #           sys.exit()

    def run(self):
        while 1:
            self.check_events()
            self.check_results()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
