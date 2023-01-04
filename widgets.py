import chess_piece as cp
from settings import *


class Widget:
    widget_list = []

    def __init__(self, game, xy: list, *, image: pg.Surface = None, text=None, func=None, width=None, height=None,
                 text_color=(5, 5, 5), background_color=(0, 135, 0), background=False, one_time_use=False,
                 show=True, text_func=None, random_variable=None):
        """SHEEESH \n
        take the rect of the "width, height" first then the "image" one then the "text" one for now"""
        Widget.widget_list.append(self)
        self.game = game
        self._xy = xy
        self._background = background
        self._background_color = background_color
        self._one_time_use = one_time_use
        self._show = show
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        if image is not None:
            self._image = image
        if text is not None:
            self._font = pg.font.SysFont("Arial", 24)
            self._text = self._font.render(text, True, text_color)
            self.string_text = text
            self.text_color = text_color
        if func is not None:
            self._func = func
        if hasattr(self, "_width") and hasattr(self, "_height"):
            self._rect = pg.Rect(xy[0], xy[1], width, height)
        elif hasattr(self, "_image"):
            self._rect = self._image.get_rect()
            self._rect.topleft = self.xy
        elif hasattr(self, "_text"):
            self._rect = self._text.get_rect()
            self._rect.topleft = self.xy
        if text_func is not None:
            self.text_func = text_func
        self.was_clicked = False
        self.random_variable = random_variable

    @property
    def xy(self):
        return self._xy

    def hide(self):
        self._show = False

    def show(self):
        self._show = True

    def update(self):
        mouse_x_y = pg.mouse.get_pos()
        if self._show:
            if hasattr(self, '_rect'):
                if self._rect.collidepoint(mouse_x_y[0], mouse_x_y[1]) and pg.mouse.get_pressed()[0]:
                    if not self.was_clicked:
                        if hasattr(self, "_func"):
                            self._func()
                        if hasattr(self, 'text_func'):
                            self.string_text = self.text_func(self.string_text)
                            self._text = self._font.render(self.string_text, True, self.text_color)
                            if not hasattr(self, '_image') and hasattr(self, '_text'):
                                self._rect.width = self._text.get_width()
                                self._rect.height = self._text.get_height()
                        if self._one_time_use:
                            self._show = False
                        self.was_clicked = True
                elif not pg.mouse.get_pressed()[0]:
                    self.was_clicked = False
            if hasattr(self, "_rect") and self._background:
                pg.draw.rect(self.game.screen, self._background_color, self._rect)
            if hasattr(self, "_image"):
                self.game.screen.blit(self._image, (self.xy[0], self.xy[1]))
            if hasattr(self, "_text"):
                self.game.screen.blit(self._text, (self.xy[0], self.xy[1]))


def add_piece():
    pass  # flemme


def set_widgets(game):
    d = cp.dict_of_chess_pieces_image
    Widget(game, [10, HEIGHT], text='This is text', text_color=(255, 255, 255))
    for color, y in zip('wb', (0, 1)):
        for piece, x in zip('kqrbnp', range(1, 7, 1)):
            image = pg.image.load(d[color][piece])
            image = pg.transform.scale(image, [30, 30])
            Widget(game, [10 + x * 34, 530 + 34 * y], image=image, background=True, background_color=(0, 110, 190),
                   show=True)


#    Widget(game, [WIDTH, HEIGHT], text='0', text_color=(1, 100, 220), text_func=lambda text: str(int(text) + 1))

# for now it's true but will need to say
# func = if piece is taken show bruh OR you display the number à côté de l'image pour afficher le nb de
# cette pièce qui a été capturée


class ColorPickWidget(Widget):
    def __init__(self, game, xy: list, *, image: pg.Surface = None, text=None, func=None, width=None, height=None,
                 text_color=(5, 5, 5), background_color=(0, 135, 0), background=False, one_time_use=False,
                 show=True, text_func=None, random_variable=None, color_func=None):
        super().__init__(game, xy, image=image, text=text, func=func, width=width, height=height,
                         text_color=text_color, background_color=background_color, background=background,
                         one_time_use=one_time_use, show=show, text_func=text_func, random_variable=random_variable)
        if color_func is not None:
            self.color_func = color_func

    def update(self):
        mouse_x_y = pg.mouse.get_pos()
        if self._show:
            if hasattr(self, '_rect'):
                if self._rect.collidepoint(mouse_x_y[0], mouse_x_y[1]) and pg.mouse.get_pressed()[0]:
                    if hasattr(self, "_func"):
                        self._func()
                    if hasattr(self, 'text_func'):
                        self.string_text = self.text_func(self.string_text)
                        self._text = self._font.render(self.string_text, True, self.text_color)
                    if hasattr(self, 'color_func'):
                        self._background_color = self.color_func()
                        if not hasattr(self, '_image') and hasattr(self, '_text'):
                            self._rect.width = self._text.get_width()
                            self._rect.height = self._text.get_height()
                    if self._one_time_use:
                        self._show = False
                elif not pg.mouse.get_pressed()[0]:
                    self.was_clicked = False
            if hasattr(self, "_rect") and self._background:
                pg.draw.rect(self.game.screen, self._background_color, self._rect)
            elif hasattr(self, "_image"):
                self.game.screen.blit(self._image, (self.xy[0], self.xy[1]))
            elif hasattr(self, "_text"):
                self.game.screen.blit(self._text, (self.xy[0], self.xy[1]))


rgb_color2pick_image = pg.image.load('ressources/rgb_color1pick.png')
rgb_color2pick_image = pg.transform.scale(rgb_color2pick_image, (127, 127))
rgb_color1pick_image = pg.image.load('ressources/rgb_color2pick.png')
rgb_color1pick_image = pg.transform.scale(rgb_color1pick_image, (127, 127))
rgb_color3pick_image = pg.image.load('ressources/rgb_color2pick.png')
rgb_color3pick_image = pg.transform.scale(rgb_color3pick_image, (127, 127))
