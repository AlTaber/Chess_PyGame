from UI_Engine import load_image
import pygame as pg

class Piece:
    def __init__(self, color, board):
        self.color = color
        self.board = board
        self.moved = False

        image = load_image(f"{color}_{self.__class__.__name__.lower()}.png")
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.transform.smoothscale(image, (self.board.cell_size, self.board.cell_size))
        self.board.all_sprites.add(self.sprite)

    def get_valid_moves(self, pos):
        pass


class Pawn(Piece):
    def get_valid_moves(self, pos):
        pass


class Rook(Piece):
    def get_valid_moves(self, pos):
        pass


class Bishop(Piece):
    def get_valid_moves(self, pos):
        pass


class Queen(Piece):
    def get_valid_moves(self, pos):
        pass


class Knight(Piece):
    def get_valid_moves(self, pos):
        pass


class King(Piece):
    def get_valid_moves(self, pos):
        pass


class Board:
    def __init__(self, parent, first_player, position, cell_size,
                 black_cell_color = pg.color.Color(20, 20, 20),
                 white_cell_color = pg.color.Color(240, 240, 240)):
        self.parent = parent

        self.position = self.left, self.top= position
        self.cell_size = cell_size

        self.black_cell_color = black_cell_color
        self.white_cell_color = white_cell_color

        self.grid = [[None for _ in range(8)] for _ in range(8)]

        self.all_sprites = pg.sprite.Group()

        self.first_player = first_player
        self.setup_pieces(first_player)

    def setup_pieces(self, first_player):
        second_player = 'white' if first_player == 'black' else 'black'
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        if first_player == "black": order[3], order[4] = order[4], order[3]
        for i, cls in enumerate(order):
            self.grid[0][i] = cls(second_player, self)
            self.grid[1][i] = Pawn(second_player, self)
            self.grid[6][i] = Pawn(first_player, self)
            self.grid[7][i] = cls(first_player, self)
        
        for i in [0, 1, 6, 7]:
            for j in range(8):
                self.grid[i][j].sprite.rect = self.grid[i][j].sprite.image.get_rect()
                self.grid[i][j].sprite.rect.topleft = self.left + j * self.cell_size, \
                                                      self.top + i * self.cell_size
    
    def render(self, surf):
        for i in range(8):
            for j in range(8):
                color = self.white_cell_color if (i + j) % 2 == 0 else self.black_cell_color
                pg.draw.rect(surf, color, pg.Rect(self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

        files = list("abcdefgh")
        ranks = list("12345678")

        f_list, r_list = files, ranks[::-1]
        if self.first_player == 'black':
            f_list, r_list = files[::-1], ranks

        font = pg.font.Font(None, 28)

        r = (self.black_cell_color.r + self.white_cell_color.r) // 2
        g = (self.black_cell_color.g + self.white_cell_color.g) // 2
        b = (self.black_cell_color.b + self.white_cell_color.b) // 2
        color = pg.Color(r, g, b)
        
        for i, f in enumerate(f_list):
            t = font.render(f, True, color)
            surf.blit(t, (self.left + i * self.cell_size + self.cell_size // 2 - t.get_width() // 2, self.top + 8 * self.cell_size))
        
        for i,r in enumerate(r_list):
            t = font.render(r, True, color)
            surf.blit(t, (self.left - t.get_width() - 10, self.top + i * self.cell_size + self.cell_size // 2 - t.get_height() // 2))

        self.all_sprites.draw(surf)
    
    def update_sprites(self):
        for i in range(8):
            for j in range(8):
                p = self.grid[i][j]
                if p: p.sprite.rect.topleft=(self.left + j * self.cell_size, self.top + i * self.cell_size)
    
    def get_motion(self, mouse_pos):
        pass

    def get_click(self, mouse_pos):
        pass

    def get_cell(self, mouse_pos):
        pass

    def on_board(self, pos):
        pass

    def is_empty(self, pos):
        pass

    def is_enemy(self, pos, color):
        pass

    def is_friendly(self, pos, color):
        pass

    def move_piece(self, start, end):
        pass

    def _castle(self, color, kingside):
        pass

    def can_castle_kingside(self, color):
        pass

    def can_castle_queenside(self, color):
        pass