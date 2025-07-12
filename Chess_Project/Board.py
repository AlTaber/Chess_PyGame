from PyQt5.QtCore import QEvent
from UI_Engine import load_image
import pygame as pg


class Piece:
    def __init__(self, color, board, sprite_dir):
        self.color = color
        self.board = board
        self.moved = False

        name = {1: 'white', -1: 'black'}[color]
        image = pg.image.load(f"assets/images/{name}_{self.__class__.__name__.lower()}.png")
        self.sprite = pg.sprite.Sprite()
        self.sprite.image = pg.transform.smoothscale(image, (self.board.cell_size, self.board.cell_size))
        if sprite_dir:
            self.board.all_sprites.add(self.sprite)
        else:
            if color == 1:
                self.board.white_prom_sprites.add(self.sprite)
            else:
                self.board.black_prom_sprites.add(self.sprite)


class Pawn(Piece):
    def __init__(self, color, board, sprite_dir):
        super().__init__(color, board, sprite_dir)
        self.direction = -self.color * self.board.player_one # Направление движения пешки
        self.moves_direction = [(0, self.direction)] # Направление ходов НЕ НА ВСЮ ДОСКУ

    def get_valid_moves(self, pos): # Показывает возможные ходы при выделении фигуры
        valid_moves = []
        for i in (-1, 1):
            if 0 <= pos[0] + i <= 7 and self.board.grid[pos[1] + self.direction][pos[0] + i] is not None and self.board.grid[pos[1] + self.direction][pos[0] + i].color != self.color:
                if pos[1] + self.direction in (0, 7):
                    valid_moves += [(pos[0] + i, pos[1] + self.direction, 5)] # 5: ход приводит к взятию + превращению пешки
                else:
                    valid_moves += [(pos[0] + i, pos[1] + self.direction, 1)] # 1: ход приводит к взятию
        for i in range(1, 3 - self.moved):
            if self.board.grid[pos[1] + self.direction * i][pos[0]] is None:
                if pos[1] + self.direction in (0, 7):
                    valid_moves += [(pos[0], pos[1] + self.direction, 4)] # 4: просто превращение пешки
                else:
                    valid_moves += [(pos[0], pos[1] + self.direction * i, 0)] # 0: ход приводит к продвижению пешки
            else:
                break # Если нельзя походить вперёд на одну клетку, то на две тем более
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
    def __init__(self, color, board, sprite_dir):
        super().__init__(color, board, sprite_dir)
        self.moves_direction = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Направление ходов НА ВСЮ ДОСКУ

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        valid_moves += [(move[0], move[1], 0)]
                    elif self.board.grid[move[1]][move[0]].color != self.color:
                        valid_moves += [(move[0], move[1], 1)]
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
    def __init__(self, color, board, sprite_dir):
        super().__init__(color, board, sprite_dir)
        self.moves_direction = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        valid_moves += [(move[0], move[1], 0)]
                    elif self.board.grid[move[1]][move[0]].color != self.color:
                        valid_moves += [(move[0], move[1], 1)]
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
    def __init__(self, color, board, sprite_dir):
        super().__init__(color, board, sprite_dir)
        self.moves_direction = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (0, -1), (-1, 0)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            for j in range(1, 8):
                move = (pos[0] + i[0] * j, pos[1] + i[1] * j)
                if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                    if self.board.grid[move[1]][move[0]] is None:
                        valid_moves += [(move[0], move[1], 0)]
                    elif self.board.grid[move[1]][move[0]].color != self.color:
                        valid_moves += [(move[0], move[1], 1)]
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
    def __init__(self, color, board, sprite_dir):
        super().__init__(color, board, sprite_dir)
        self.moves_direction = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            move = (pos[0] + i[0], pos[1] + i[1])
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if self.board.grid[move[1]][move[0]] is None:
                    valid_moves += [(move[0], move[1], 0)]
                elif self.board.grid[move[1]][move[0]].color != self.color:
                    valid_moves += [(move[0], move[1], 1)]
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
    def __init__(self, color, board, sprite_dir):
        super().__init__(color, board, sprite_dir)
        self.moves_direction = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]

    def get_valid_moves(self, pos):
        valid_moves = []
        for i in self.moves_direction:
            move = (pos[0] + i[0], pos[1] + i[1])
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7 and move not in self.board.attack_grid: # Не выходим за доску и на подбитые поля
                if self.board.grid[move[1]][move[0]] is None:
                    valid_moves += [(move[0], move[1], 0)]
                elif self.board.grid[move[1]][move[0]].color != self.color:
                    valid_moves += [(move[0], move[1], 1)]
        if not self.moved and self.board.can_castle_king_side(self.color):
            valid_moves += [(pos[0] + 2 * self.board.player_one, pos[1], 2)]
        if not self.moved and self.board.can_castle_queen_side(self.color):
            valid_moves += [(pos[0] - 2 * self.board.player_one, pos[1], 3)]
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

        self.white_prom_sprites = pg.sprite.Group() # Спрайт выбора ферзя / ладьи / коня / слона
        self.black_prom_sprites = pg.sprite.Group() # То же, для другого цвета
        self.prom_holder = []
        self.prom_square = tuple() # Если пусто, то превращения нет, иначе - координаты превращения

        self.color_to_move = 1 # Какой цвет сейчас ходит (1 - Белый, -1 - Чёрный)
        self.player_one = first_player # Какими фигурами играет игрок 1 (тот, что снизу)
        self.setup_pieces(first_player)

    def setup_pieces(self, first_player): # Расставляем фигуры при начале игры
        second_player = 1 if first_player == -1 else -1
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        prom_order = [Rook, Knight, Bishop, Queen]
        for index, i in enumerate(prom_order):
            self.prom_holder += [i(1, self, False)]
            self.prom_holder += [i(-1, self, False)]
        if first_player == -1: order[3], order[4] = order[4], order[3]
        for i, cls in enumerate(order):
            self.grid[0][i] = cls(second_player, self, True)
            self.grid[1][i] = Pawn(second_player, self, True)
            self.grid[6][i] = Pawn(first_player, self, True)
            self.grid[7][i] = cls(first_player, self, True)

        for i in [0, 1, 6, 7]:
            for j in range(8):
                self.grid[i][j].sprite.rect = self.grid[i][j].sprite.image.get_rect()
                self.grid[i][j].sprite.rect.topleft = self.left + j * self.cell_size, \
                                                      self.top + i * self.cell_size
        for i in range(4):
            self.prom_holder[i * 2].sprite.rect = self.prom_holder[i * 2].sprite.image.get_rect()
            self.prom_holder[i * 2].sprite.rect.topleft = self.left + (
                        i + 2) * self.cell_size, self.top + 3 * self.cell_size
            self.prom_holder[i * 2 + 1].sprite.rect = self.prom_holder[i * 2 + 1].sprite.image.get_rect()
            self.prom_holder[i * 2 + 1].sprite.rect.topleft = self.left + (
                        i + 2) * self.cell_size, self.top + 3 * self.cell_size

    def render(self, surf): # Отрисовываем доску каждый кадр
        for i in range(8):
            for j in range(8):
                if self.active_cell == (j, i) and self.grid[i][j] is not None: # Выбор цвета для активной/обычной клетки
                    color = self.white_active_color if (i + j) % 2 == 0 else self.black_active_color
                else:
                    color = self.white_cell_color if (i + j) % 2 == 0 else self.black_cell_color
                pg.draw.rect(surf, color, pg.Rect(self.left + j * self.cell_size,
                                                  self.top + i * self.cell_size, self.cell_size, self.cell_size))

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

        if self.prom_square:
            if self.color_to_move == 1:
                self.white_prom_sprites.draw(surf)
            else:
                self.black_prom_sprites.draw(surf)
        else:
            for i in self.valid_moves: # Отрисовка мест, куда можно походить
                pg.draw.circle(surf, self.gray_color, (self.left + i[0] * self.cell_size + self.cell_size // 2,
                                                              self.top + i[1] * self.cell_size + self.cell_size // 2),
                                                                  self.cell_size // (5 if i[-1] else 10))
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
        if self.prom_square:
            d = {2: Rook, 3: Knight, 4: Bishop, 5: Queen}
            if clicked_cell[0] in d and clicked_cell[1] == 3:
                if self.prom_square[4] == 5:
                    self.grid[self.prom_square[1]][self.prom_square[0]].sprite.kill()
                    print(f"{self.grid[self.prom_square[1]][self.prom_square[0]].__class__.__name__} was captured!")
                self.grid[self.prom_square[1]][self.prom_square[0]] = d[clicked_cell[0]](self.color_to_move, self, True)
                new_obj = self.grid[self.prom_square[1]][self.prom_square[0]]
                new_obj.sprite.rect = new_obj.sprite.image.get_rect()
                new_obj.sprite.rect.topleft = (self.left + self.prom_square[0] * self.cell_size,
                                               self.top + self.prom_square[1] * self.cell_size)
                self.grid[self.prom_square[3]][self.prom_square[2]].sprite.kill()
                self.grid[self.prom_square[3]][self.prom_square[2]] = None
                self.check_attacks()
                self.color_to_move = -self.color_to_move
            self.prom_square = tuple()
            return
        if self.active_cell is not None:
            for i in (0, 1, 2, 3, 4, 5):
                if (clicked_cell[0], clicked_cell[1], i) in self.valid_moves:
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

    def check_attacks(self):
        self.attack_grid = set()
        for i in range(8):
            for j in range(8):
                if self.grid[i][j] is not None:
                    self.attack_grid.update(self.grid[i][j].get_attacks((j, i), self.color_to_move))

    def move_piece(self, start, end, action):
        if action == 1: # Поимка фигуры (возможно и с превращением пешки)
            self.grid[end[1]][end[0]].sprite.kill()
            print(f"{self.grid[end[1]][end[0]].__class__.__name__} was captured!")
        elif action == 2: # Двигаем ладью при королевской рокировке
            self.grid[end[1]][end[0] + self.player_one], self.grid[end[1]][end[0] - self.player_one] = None, self.grid[
                end[1]][end[0] + self.player_one]
        elif action == 3: # Двигаем ладью при ферзевой рокировке
            self.grid[end[1]][end[0]-2*self.player_one], self.grid[end[1]][end[0] + self.player_one] = None, self.grid[
                end[1]][end[0] - 2 * self.player_one]
        if action in (4, 5):
            self.prom_square = (end[0], end[1], start[0], start[1], action)
            return
        self.grid[start[1]][start[0]].moved = True
        self.grid[start[1]][start[0]], self.grid[end[1]][end[0]] = None, self.grid[start[1]][start[0]] # Двигаем фигуру
        self.check_attacks()
        self.color_to_move = -self.color_to_move # Объявляем ход следующего игрока
        self.update_sprites() # Отрисовываем спрайты после хода

    def can_castle_king_side(self, color):
        side = {1: 7, -1: 0}[color * self.player_one] # Получаем сторону, где рокировка
        fix = {1: (7, 5, 7), -1: (0, 1, 3)}[self.player_one] # Учитываем (долбанные) особенности сторон цветов
        if (self.grid[side][fix[0]] is not None and self.grid[side][fix[0]].moved) or self.grid[side][fix[0]] is None:
            return False
        for i in range(fix[1], fix[2]):
            if self.grid[side][i] is not None or (i, side) in self.attack_grid:
                return False
        return True

    def can_castle_queen_side(self, color):
        side = {1: 7, -1: 0}[color * self.player_one]
        fix = {1: (0, 1, 4), -1: (7, 4, 7)}[self.player_one]
        if (self.grid[side][fix[0]] is not None and self.grid[side][fix[0]].moved) or self.grid[side][fix[0]] is None:
            return False
        for i in range(fix[1], fix[2]):
            if self.grid[side][i] is not None or (i, side) in self.attack_grid:
                return False
        return True