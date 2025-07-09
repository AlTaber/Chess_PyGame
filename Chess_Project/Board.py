from UI_Engine import load_image
import pygame as pg


class Piece:
    def __init__(self, color, board):
        self.color = {"white": 1, "black": -1}[color]
        self.board = board
        self.moved = False

        image = load_image(f"{color}_{self.__class__.__name__.lower()}.png")
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.transform.smoothscale(image, (self.board.cell_size, self.board.cell_size))
        self.board.all_sprites.add(self.sprite)


class Pawn(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.direction = -self.color * {"white": 1, "black": -1}[self.board.player_one] # Направление движения пешки
        self.moves_direction = [(0, self.direction)] # Список направлений, куда ходит фигура (Не на всю доску)

    def get_valid_moves(self, pos): # Показывает возможные ходы при выделении фигуры
        valid_moves = []
        for i in (-1, 1):
            if 0 <= pos[0] + i <= 7 and self.board.grid[pos[1] + self.direction][pos[0] + i] is not None and self.board.grid[pos[1] + self.direction][pos[0] + i].color != self.color:
                valid_moves += [(pos[0] + i, pos[1] + self.direction, True)] # True: ход приводит к взятию
        for i in range(1, 3 - self.moved):
            if self.board.grid[pos[1] + self.direction * i][pos[0]] is None:
                valid_moves += [(pos[0], pos[1] + self.direction * i, False)] # False: ход просто двигает фигуру
            else:
                break
        return valid_moves # Координаты клеток, куда в итоге можно вообще пойти

    def get_attacks(self, pos, color): # Показывает клетки под боем для вражеского короля
        attacks = set()
        if self.color != color: # Если фигура одного цвета с вражеским королём - не берём её в расчёт
            return attacks
        for i in (-1, 1):
            if 0 <= pos[0] + i <= 7:
                attacks.add((pos[0] + i, pos[1] + self.direction))
        return attacks # Координаты клеток, куда вражеский король не пойдёт


class Rook(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.moves_direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        valid_moves += [(move[0], move[1], False)]
                    elif self.board.grid[move[1]][move[0]].color != self.color:
                        valid_moves += [(move[0], move[1], True)]
                        break
                    else:
                        break
                else:
                    break
        return valid_moves

    def get_attacks(self, pos, color):
        attacks = set()
        if self.color != color:
            return attacks
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        attacks.add((move[0], move[1]))
                    elif self.board.grid[move[1]][move[0]].color == self.color:
                        attacks.add((move[0], move[1]))
                        break
                else:
                    break
        return attacks


class Bishop(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.moves_direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        valid_moves += [(move[0], move[1], False)]
                    elif self.board.grid[move[1]][move[0]].color != self.color:
                        valid_moves += [(move[0], move[1], True)]
                        break
                    else:
                        break
                else:
                    break
        return valid_moves

    def get_attacks(self, pos, color):
        attacks = set()
        if self.color != color:
            return attacks
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        attacks.add((move[0], move[1]))
                    elif self.board.grid[move[1]][move[0]].color == self.color:
                        attacks.add((move[0], move[1]))
                        break
                else:
                    break
        return attacks


class Queen(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.moves_direction = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        valid_moves += [(move[0], move[1], False)]
                    elif self.board.grid[move[1]][move[0]].color != self.color:
                        valid_moves += [(move[0], move[1], True)]
                        break
                    else:
                        break
                else:
                    break
        return valid_moves

    def get_attacks(self, pos, color):
        attacks = set()
        if self.color != color:
            return attacks
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        attacks.add((move[0], move[1]))
                    elif self.board.grid[move[1]][move[0]].color == self.color:
                        attacks.add((move[0], move[1]))
                        break
                else:
                    break
        return attacks

class Knight(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.moves_direction = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            move = (pos[0] + i[0], pos[1] + i[1])
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if self.board.grid[move[1]][move[0]] is None:
                    valid_moves += [(move[0], move[1], False)]
                elif self.board.grid[move[1]][move[0]].color != self.color:
                    valid_moves += [(move[0], move[1], True)]
        return valid_moves

    def get_attacks(self, pos, color):
        attacks = set()
        if self.color != color:
            return attacks
        for i in self.moves_direction:
            move = (pos[0] + i[0], pos[1] + i[1])
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                attacks.add(move)
        return attacks


class King(Piece):
    def __init__(self, color, board):
        super().__init__(color, board)
        self.moves_direction = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            move = (pos[0] + i[0], pos[1] + i[1])
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7 and move not in self.board.attack_grid: # Не выходим за доску и на подбитые поля
                if self.board.grid[move[1]][move[0]] is None:
                    valid_moves += [(move[0], move[1], False)]
                elif self.board.grid[move[1]][move[0]].color != self.color:
                    valid_moves += [(move[0], move[1], True)]
        return valid_moves

    def get_attacks(self, pos, color):
        attacks = set()
        if self.color != color:
            return attacks
        for i in self.moves_direction:
            move = (pos[0] + i[0], pos[1] + i[1])
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                attacks.add(move)
        return attacks


class Board:
    def __init__(self, parent, first_player, position, cell_size,
                 black_cell_color = pg.color.Color(20, 20, 20),
                 white_cell_color = pg.color.Color(240, 240, 240)):
        self.parent = parent

        self.position = self.left, self.top= position
        self.cell_size = cell_size

        self.black_cell_color = black_cell_color # Цвет белых клеток
        self.white_cell_color = white_cell_color # Цвет чёрных клеток
        self.black_active_color = pg.Color(200, 200, 0) # Базовый цвет активной клеточки, который позже перемешаем с чёрным
        self.white_active_color = pg.Color(200, 200, 0) # То же, но перемешаем с белым
        self.gray_color = pg.color.Color(0, 0, 0) # Средний цвет между белым и чёрным
        for i in range(3):
            self.black_active_color[i] = (self.black_active_color[i] + black_cell_color[i]) // 2
            self.white_active_color[i] = (self.white_active_color[i] + white_cell_color[i]) // 2
            self.gray_color[i] = (self.black_cell_color[i] + self.white_cell_color[i]) // 2

        self.grid = [[None for _ in range(8)] for _ in range(8)] # Расположение фигур на доске
        self.attack_grid = set() # Клеточки, куда нельзя походить королю в свой ход
        self.valid_moves = [] # Список возможных ходов фигуры, стоящей на выделенной клеточке
        self.active_cell = None # Выделенная мышкой клеточка

        self.all_sprites = pg.sprite.Group()

        self.color_to_move = 1 # Какой цвет щас ходит (1 - Белый, -1 - Чёрный)
        self.player_one = first_player # Какими фигурами играет игрок 1 (тот, что снизу)
        self.setup_pieces(first_player)

    def setup_pieces(self, first_player): # Расставляем фигуры при начале игры
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
    
    def render(self, surf): # Отрисовываем доску каждый кадр
        for i in range(8):
            for j in range(8):
                if self.active_cell == (j, i) and self.grid[i][j] is not None: # Выбор цвета для активной/обычной клетки
                    color = self.white_active_color if (i + j) % 2 == 0 else self.black_active_color
                else:
                    color = self.white_cell_color if (i + j) % 2 == 0 else self.black_cell_color
                pg.draw.rect(surf, color, pg.Rect(self.left + j * self.cell_size, self.top + i * self.cell_size, self.cell_size, self.cell_size))

        if self.active_cell is not None: # Отрисовка мест, куда можно походить
            for i in self.valid_moves:
                pg.draw.circle(surf, self.gray_color, (self.left + i[0] * self.cell_size + self.cell_size // 2,
                                                              self.top + i[1] * self.cell_size + self.cell_size // 2),
                                                              self.cell_size // (5 if i[-1] else 10))

        files = list("abcdefgh")
        ranks = list("12345678")

        f_list, r_list = files, ranks[::-1]
        if self.player_one == 'black':
            f_list, r_list = files[::-1], ranks

        font = pg.font.Font(None, 28)
        text_color = self.gray_color
        
        for i, f in enumerate(f_list):
            t = font.render(f, True, text_color)
            surf.blit(t, (self.left + i * self.cell_size + self.cell_size // 2 - t.get_width() // 2, self.top + 8 * self.cell_size))
        
        for i,r in enumerate(r_list):
            t = font.render(r, True, text_color)
            surf.blit(t, (self.left - t.get_width() - 10, self.top + i * self.cell_size + self.cell_size // 2 - t.get_height() // 2))

        self.all_sprites.draw(surf)
    
    def update_sprites(self): # Обновляем спрайты
        for i in range(8):
            for j in range(8):
                p = self.grid[i][j]
                if p:
                    p.sprite.rect.topleft = (self.left + j * self.cell_size, self.top + i * self.cell_size)
    
    def get_motion(self, mouse_pos): # Подсвечивание возможных ходов наведением курсора (WIP)
        pass

    def get_click(self, mouse_pos): # Разбираемся: выделяем ли клетку, отменяем ли выделение или ходим
        clicked_cell = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.top) // self.cell_size)
        if self.active_cell is not None:
            for i in (False, True):
                if (clicked_cell[0], clicked_cell[1], i) in self.valid_moves: # True: забираем фигуру, False: просто ходим
                    self.move_piece(self.active_cell, clicked_cell, i)
                    self.active_cell = None
                    self.valid_moves = []
                    return
        if (not (0 <= clicked_cell[0] <= 7) or not (0 <= clicked_cell[1] <= 7) or
                self.grid[clicked_cell[1]][clicked_cell[0]] is None or
                self.grid[clicked_cell[1]][clicked_cell[0]].color != self.color_to_move): # Отменяем выделение
            self.valid_moves = []
            self.active_cell = None
            return
        self.active_cell = clicked_cell # Записываем выделенную клетку и получаем координаты возможных ходов
        self.valid_moves = self.grid[self.active_cell[1]][self.active_cell[0]].get_valid_moves(self.active_cell)

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

    def move_piece(self, start, end, action):
        if action: # True - Выполняем действие при поимке фигуры
            self.grid[end[1]][end[0]].sprite.kill()
            print(f"{self.grid[end[1]][end[0]].__class__.__name__} was captured!")
        self.grid[start[1]][start[0]], self.grid[end[1]][end[0]] = None, self.grid[start[1]][start[0]] # Двигаем фигуру
        self.attack_grid = set() # Ситуация поменялась, проверяем подбитые поля для короля по новой.
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] is not None:
                    self.attack_grid.update(self.grid[i][j].get_attacks((j, i), self.color_to_move)) # Добавляем запрещённые ходы королю
        self.color_to_move = -self.color_to_move # Объявляем ход следующего игрока
        self.update_sprites() # Отрисовываем спрайты после хода

    def _castle(self, color, side): # Рокировка (WIP)
        pass

    def can_castle_king_side(self, color): # Проверка на рокировку на королевский фланг (WIP)
        pass

    def can_castle_queen_side(self, color): # Проверка на рокировку на ферзевой фланг (WIP)
        pass