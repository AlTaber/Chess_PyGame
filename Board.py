from UI_Engine import load_image
import pygame as pg
import time
import sys
import threading
import os

pg.mixer.init()


try:
    move_sound = pg.mixer.Sound("Assets/sounds/move.wav")
    capture_sound = pg.mixer.Sound("Assets/sounds/capture.wav")
    check_sound = pg.mixer.Sound("Assets/sounds/check.wav")
    castle_sound = pg.mixer.Sound("Assets/sounds/castle.wav")
    end_sound = pg.mixer.Sound("Assets/sounds/end.wav")
    bg_music = pg.mixer.Sound("Assets/sounds/bg.mp3")

    # Настройка громкости
    move_sound.set_volume(0.5)
    capture_sound.set_volume(0.7)
    check_sound.set_volume(0.6)
    castle_sound.set_volume(0.6)
    end_sound.set_volume(0.8)
    bg_music.set_volume(0.3)

    # Флаг успешной загрузки звуков
    sounds_loaded = True
except:
    # Создание заглушек для звуков
    move_sound = pg.mixer.Sound(buffer=bytearray([128] * 8000))
    capture_sound = pg.mixer.Sound(buffer=bytearray([128] * 12000))
    check_sound = pg.mixer.Sound(buffer=bytearray([128] * 16000))
    castle_sound = pg.mixer.Sound(buffer=bytearray([128] * 10000))
    end_sound = pg.mixer.Sound(buffer=bytearray([128] * 20000))
    bg_music = pg.mixer.Sound(buffer=bytearray([128] * 40000))
    sounds_loaded = False


class ChessTimer:
    def __init__(self):
        # Настройки таймера
        self.INITIAL_TIME = 300  # 5 минут в секундах
        self.white_time = self.INITIAL_TIME
        self.black_time = self.INITIAL_TIME
        self.active_player = 1  # 1 - белые, 2 - черные
        self.last_update_time = time.time()
        self.game_active = True
        self.running = True

        # Цвета
        self.BACKGROUND = (30, 30, 40)
        self.PLAYER1_BG = (50, 50, 70)
        self.PLAYER2_BG = (50, 50, 70)
        self.ACTIVE_BG = (70, 100, 120)
        self.TEXT_COLOR = (220, 220, 220)
        self.WARNING_COLOR = (220, 80, 60)
        self.INFO_COLOR = (100, 180, 255)

        # Шрифты
        self.font_large = pg.font.SysFont('Arial', 48, bold=True)
        self.font_medium = pg.font.SysFont('Arial', 24)
        self.font_small = pg.font.SysFont('Arial', 18)

        # Запуск потока обновления времени
        self.timer_thread = threading.Thread(target=self.update_loop)
        self.timer_thread.daemon = True
        self.timer_thread.start()

    def update_loop(self):
        """Цикл обновления времени каждую секунду"""
        while self.running:
            time.sleep(1.0)  # Точное обновление каждую секунду
            if self.game_active:
                self.update()

    def reset(self):
        self.white_time = self.INITIAL_TIME
        self.black_time = self.INITIAL_TIME
        self.game_active = True
        self.last_update_time = time.time()

    def start_game(self, starting_player=1):
        self.reset()
        self.active_player = 1 if starting_player == 1 else 2

    def switch_turn(self):
        if not self.game_active:
            return

        # Переключение активного игрока
        self.active_player = 3 - self.active_player  # Переключает 1->2 или 2->1
        self.last_update_time = time.time()

    def update(self):
        if not self.game_active:
            return

        current_time = time.time()
        delta_time = current_time - self.last_update_time

        # Обновление времени активного игрока
        if self.active_player == 1:
            self.white_time = max(0, self.white_time - delta_time)
            if self.white_time <= 0:
                self.game_active = False
        else:
            self.black_time = max(0, self.black_time - delta_time)
            if self.black_time <= 0:
                self.game_active = False

        self.last_update_time = current_time

    def format_time(self, seconds):
        """Форматирование времени в MM:SS"""
        mins = int(seconds) // 60
        secs = int(seconds) % 60
        return f"{mins:02d}:{secs:02d}"

    def draw_white(self, surface, x, y, width, height):
        """Отрисовка таймера белых"""
        # Фон таймера
        bg_color = self.ACTIVE_BG if self.active_player == 1 else self.PLAYER1_BG
        rect = pg.Rect(x, y, width, height)
        pg.draw.rect(surface, bg_color, rect, 0, 10)
        pg.draw.rect(surface, (100, 100, 130), rect, 3, 10)  # Обводка

        # Время
        time_color = self.WARNING_COLOR if self.white_time < 30 and self.active_player == 1 else self.TEXT_COLOR
        time_text = self.font_large.render(self.format_time(self.white_time), True, time_color)
        time_rect = time_text.get_rect(center=(rect.centerx, rect.centery))
        surface.blit(time_text, time_rect)

        # Подпись заменена на пробел
        label = self.font_small.render(" ", True, self.INFO_COLOR)
        label_rect = label.get_rect(center=(rect.centerx, rect.top + 15))
        surface.blit(label, label_rect)

    def draw_black(self, surface, x, y, width, height):
        """Отрисовка таймера черных"""
        # Фон таймера
        bg_color = self.ACTIVE_BG if self.active_player == 2 else self.PLAYER2_BG
        rect = pg.Rect(x, y, width, height)
        pg.draw.rect(surface, bg_color, rect, 0, 10)
        pg.draw.rect(surface, (100, 100, 130), rect, 3, 10)  # Обводка

        # Время
        time_color = self.WARNING_COLOR if self.black_time < 30 and self.active_player == 2 else self.TEXT_COLOR
        time_text = self.font_large.render(self.format_time(self.black_time), True, time_color)
        time_rect = time_text.get_rect(center=(rect.centerx, rect.centery))
        surface.blit(time_text, time_rect)

        # Подпись заменена на пробел
        label = self.font_small.render(" ", True, self.INFO_COLOR)
        label_rect = label.get_rect(center=(rect.centerx, rect.top + 15))
        surface.blit(label, label_rect)

    def stop(self):
        """Остановка таймера при завершении игры"""
        self.running = False

class Piece:
    def __init__(self, color, board, sprite_dir):
        self.color = color
        self.board = board
        self.moved = False

        try: # Загрузка изображения
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
        except:
            # Создание фигуры-заглушки
            self.sprite = pg.sprite.Sprite()
            self.sprite.image = pg.Surface((self.board.cell_size, self.board.cell_size))
            self.sprite.image.fill(pg.Color('red') if color == 'white' else pg.Color('blue'))
            pg.draw.circle(self.sprite.image, pg.Color('white'),
                           (self.board.cell_size // 2, self.board.cell_size // 2),
                           self.board.cell_size // 3)


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

        self.position = self.left, self.top = position[0] + 200, position[1]
        self.cell_size = cell_size

        self.black_cell_color = black_cell_color
        self.white_cell_color = white_cell_color
        self.black_active_color = pg.Color(200, 200, 0)
        self.white_active_color = pg.Color(200, 200, 0)
        self.gray_color = pg.color.Color(0, 0, 0)
        for i in range(3):
            self.black_active_color[i] = (self.black_active_color[i] + black_cell_color[i]) // 2
            self.white_active_color[i] = (self.white_active_color[i] + white_cell_color[i]) // 2
            self.gray_color[i] = (self.black_cell_color[i] + self.white_cell_color[i]) // 2

        self.grid = [[None for _ in range(8)] for _ in range(8)] # Расположение фигур на доске
        self.attack_grid = set() # Клеточки, куда нельзя походить королю в свой ход
        self.valid_moves = [] # Список возможных ходов фигуры, стоящей на выделенной клеточке
        self.active_cell = None # Выделенная мышкой клеточка

        self.all_sprites = pg.sprite.Group()

        self.white_prom_sprites = pg.sprite.Group() # Спрайты выбора ферзя / ладьи / коня / слона
        self.black_prom_sprites = pg.sprite.Group() # То же, для другого цвета
        self.prom_holder = []
        self.prom_square = tuple() # Если пусто, то превращения нет, иначе - координаты превращения

        self.color_to_move = 1 # Какой цвет сейчас ходит (1 - Белый, -1 - Чёрный)
        self.player_one = first_player # Какими фигурами играет игрок 1 (тот, что снизу)
        self.setup_pieces(first_player)

        # Материальное преимущество
        self.material_font = pg.font.Font(None, 36)
        self.white_material = 39
        self.black_material = 39
        self.captured_by_white = []  # Список съеденных белыми фигур
        self.captured_by_black = []  # Список съеденных черными фигур
        self.calculate_material()

        # Загрузка миниатюр фигур
        self.piece_miniatures = {}
        self.load_miniatures()

        # Таймер
        self.timer = ChessTimer()
        self.timer.start_game(first_player)

        # История ходов
        self.move_history = []
        self.move_font = pg.font.SysFont('Arial', 20)
        self.move_number = 1
        self.history_scroll = 0

        # Настройки таймеров
        self.timer_width = 200
        self.timer_height = 80
        self.timer_margin = 30  # Расстояние от доски до таймеров

        # Цвета для элементов интерфейса
        self.element_bg = (50, 50, 70)  # Фон как у таймеров
        self.element_border = (100, 100, 130)  # Обводка как у таймеров

    def load_miniatures(self):
        """Загрузка миниатюр фигур для отображения съеденных фигур"""
        piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen']
        colors = ['black', 'white']
        size = 20  # Размер миниатюр

        for color in colors:
            for piece in piece_types:
                try:
                    img = pg.image.load(f"assets/images/{color}_{piece}.png")
                    self.piece_miniatures[f"{color}_{piece}"] = pg.transform.smoothscale(img, (size, size))
                except:
                    # Создание заглушки
                    surf = pg.Surface((size, size), pg.SRCALPHA)
                    if color == 'white':
                        pg.draw.circle(surf, (255, 255, 255), (size // 2, size // 2), size // 3)
                    else:
                        pg.draw.circle(surf, (100, 100, 100), (size // 2, size // 2), size // 3)
                    self.piece_miniatures[f"{color}_{piece}"] = surf

    def calculate_material(self):
        self.white_material = 0
        self.black_material = 0

        piece_values = {
            Pawn: 1,
            Knight: 3,
            Bishop: 3,
            Rook: 5,
            Queen: 9,
            King: 0  # Король не имеет материальной ценности
        }

        for row in self.grid:
            for piece in row:
                if piece:
                    value = piece_values.get(type(piece), 0)
                    if piece.color == 1:
                        self.white_material += value
                    else:
                        self.black_material += value

    def get_move_notation(self, piece, start, end, capture):
        col_to_letter = lambda col: chr(ord('a') + col)
        row_to_number = lambda row: 8 - row

        start_col, start_row = start
        end_col, end_row = end

        if isinstance(piece, Pawn):
            if capture == 1:
                return f"{col_to_letter(start_col)}x{col_to_letter(end_col)}{row_to_number(end_row)}"
            elif capture == 4:
                return "Prom"
            elif capture == 5:
                return "Capture"
            else:
                return f"{col_to_letter(end_col)}{row_to_number(end_row)}"

        piece_letters = {
            Rook: 'R',
            Knight: 'N',
            Bishop: 'B',
            Queen: 'Q',
            King: 'K'
        }
        letter = piece_letters.get(type(piece), '')

        if capture == 1:
            return f"{letter}x{col_to_letter(end_col)}{row_to_number(end_row)}"
        else:
            return f"{letter}{col_to_letter(end_col)}{row_to_number(end_row)}"

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
        board_width = 8 * self.cell_size

        for i in range(8):
            for j in range(8):
                if self.active_cell == (j, i): # Выбор цвета для активной/обычной клетки
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

        # Расчет позиций таймеров (на уровне 8-го ряда)
        timer_y = self.top + 7 * self.cell_size

        # Левый таймер (белые) - выравнивание по левому краю доски
        white_timer_x = self.left - self.timer_width - self.timer_margin

        # Правый таймер (черные) - выравнивание по правому краю доски
        black_timer_x = self.left + board_width + self.timer_margin

        # Отрисовка таймеров
        self.timer.draw_white(surf, white_timer_x, timer_y, self.timer_width, self.timer_height)
        self.timer.draw_black(surf, black_timer_x, timer_y, self.timer_width, self.timer_height)

        # Материальное преимущество над таймерами
        material_y = timer_y - 40  # Располагаем над таймерами

        # Стили для отображения
        plus_color = pg.Color(100, 255, 100)  # Зеленый для плюса
        minus_color = pg.Color(180, 180, 180)  # Серый для минуса

        # Расчет материального преимущества
        white_advantage = self.white_material - self.black_material
        black_advantage = self.black_material - self.white_material

        # Для белых (Player 1)
        if white_advantage > 0:
            white_text = f"Player 1: +{white_advantage}"
            text_color_white = plus_color
        elif white_advantage < 0:
            white_text = "Player 1: --"  # Заменяем отрицательное на "--"
            text_color_white = minus_color
        else:
            white_text = "Player 1: -"
            text_color_white = minus_color

        # Создаем поверхность для текста
        white_surface = self.material_font.render(white_text, True, text_color_white)
        # Создаем фон
        white_bg_rect = pg.Rect(
            white_timer_x,
            material_y,
            self.timer_width,
            white_surface.get_height() + 10
        )
        # Отрисовываем фон и текст
        pg.draw.rect(surf, self.element_bg, white_bg_rect, 0, 5)
        pg.draw.rect(surf, self.element_border, white_bg_rect, 2, 5)
        surf.blit(white_surface,
                  (white_timer_x + self.timer_width / 2 - white_surface.get_width() / 2,
                   material_y + 5))

        # Для черных (Player 2)
        if black_advantage > 0:
            black_text = f"Player 2: +{black_advantage}"
            text_color_black = plus_color
        elif black_advantage < 0:
            black_text = "Player 2: --"  # Заменяем отрицательное на "--"
            text_color_black = minus_color
        else:
            black_text = "Player 2: -"
            text_color_black = minus_color

        # Создаем поверхность для текста
        black_surface = self.material_font.render(black_text, True, text_color_black)
        # Создаем фон
        black_bg_rect = pg.Rect(
            black_timer_x,
            material_y,
            self.timer_width,
            black_surface.get_height() + 10
        )
        # Отрисовываем фон и текст
        pg.draw.rect(surf, self.element_bg, black_bg_rect, 0, 5)
        pg.draw.rect(surf, self.element_border, black_bg_rect, 2, 5)
        surf.blit(black_surface,
                  (black_timer_x + self.timer_width / 2 - black_surface.get_width() / 2,
                   material_y + 5))

        # Отображение съеденных фигур с фоном как у таймеров
        # Увеличено расстояние до материального преимущества
        captured_y = material_y - 60  # Увеличен отступ

        # Для белых (съеденные ими черные фигуры)
        offset_x = white_timer_x
        piece_size = 20
        piece_spacing = 5

        # Создаем фон для съеденных фигур белых
        captured_white_width = self.timer_width
        captured_white_height = 60  # Высота области (для двух рядов)
        captured_white_rect = pg.Rect(
            offset_x, captured_y - 10,
            captured_white_width, captured_white_height
        )
        pg.draw.rect(surf, self.element_bg, captured_white_rect, 0, 10)
        pg.draw.rect(surf, self.element_border, captured_white_rect, 2, 10)

        # Подпись внутри фона
        capture_label = pg.font.SysFont('Arial', 14).render("           ", True, pg.Color(180, 180, 180))
        surf.blit(capture_label, (offset_x + 10, captured_y - 5))

        # Группируем съеденные фигуры по типу
        black_piece_count = {}
        for piece_type in self.captured_by_white:
            black_piece_count[piece_type] = black_piece_count.get(piece_type, 0) + 1

        # Отображаем миниатюры в два ряда
        max_per_row = 4  # Максимальное количество фигур в одном ряду
        items = list(black_piece_count.items())
        rows = []
        if len(items) > max_per_row:
            rows.append(items[:max_per_row])
            rows.append(items[max_per_row:])
        else:
            rows.append(items)

        # Отрисовка рядов
        for row_idx, row_items in enumerate(rows):
            row_y = captured_y + row_idx * (piece_size + 3)
            x_pos = offset_x + 10  # Отступ от края фона
            for piece_type, count in row_items:
                key = f"black_{piece_type.lower()}"
                if key in self.piece_miniatures:
                    surf.blit(self.piece_miniatures[key], (x_pos, row_y))

                # Отображаем количество
                count_text = pg.font.SysFont('Arial', 14).render(f"x{count}", True, pg.Color(200, 200, 200))
                surf.blit(count_text, (x_pos + piece_size + 2, row_y - 2))

                x_pos += piece_size + piece_spacing + 25

        # Для черных (съеденные ими белые фигуры)
        offset_x = black_timer_x

        # Создаем фон для съеденных фигур черных
        captured_black_rect = pg.Rect(
            offset_x, captured_y - 10,
            captured_white_width, captured_white_height
        )
        pg.draw.rect(surf, self.element_bg, captured_black_rect, 0, 10)
        pg.draw.rect(surf, self.element_border, captured_black_rect, 2, 10)

        # Подпись внутри фона
        capture_label = pg.font.SysFont('Arial', 14).render("       ", True, pg.Color(180, 180, 180))
        surf.blit(capture_label, (offset_x + 10, captured_y - 5))

        # Группируем съеденные фигуры по типу
        white_piece_count = {}
        for piece_type in self.captured_by_black:
            white_piece_count[piece_type] = white_piece_count.get(piece_type, 0) + 1

        # Отображаем миниатюры в два ряда
        items = list(white_piece_count.items())
        rows = []
        if len(items) > max_per_row:
            rows.append(items[:max_per_row])
            rows.append(items[max_per_row:])
        else:
            rows.append(items)

        # Отрисовка рядов
        for row_idx, row_items in enumerate(rows):
            row_y = captured_y + row_idx * (piece_size + 3)
            x_pos = offset_x + 10  # Отступ от края фона
            for piece_type, count in row_items:
                key = f"white_{piece_type.lower()}"
                if key in self.piece_miniatures:
                    surf.blit(self.piece_miniatures[key], (x_pos, row_y))

                # Отображаем количество
                count_text = pg.font.SysFont('Arial', 14).render(f"x{count}", True, pg.Color(200, 200, 200))
                surf.blit(count_text, (x_pos + piece_size + 2, row_y - 2))

                x_pos += piece_size + piece_spacing + 25

        # История ходов (справа от доски на уровне 1-го ряда)
        history_x = self.left + board_width + self.timer_margin
        history_y = self.top
        history_width = 250
        history_height = 280

        # Рисуем фон истории ходов
        history_bg_rect = pg.Rect(history_x, history_y, history_width, history_height)
        pg.draw.rect(surf, self.element_bg, history_bg_rect, 0, 10)
        pg.draw.rect(surf, self.element_border, history_bg_rect, 2, 10)

        # Заголовок истории ходов
        history_title = self.move_font.render("Move History:", True, pg.Color(255, 255, 255))
        surf.blit(history_title, (history_x + 10, history_y + 10))

        # Отрисовка последних 10 ходов
        start_idx = max(0, len(self.move_history) - 10 + self.history_scroll)
        visible_moves = self.move_history[start_idx:start_idx + 10]

        for i, move in enumerate(visible_moves):
            move_text = self.move_font.render(move, True, pg.Color(200, 200, 200))
            surf.blit(move_text, (history_x + 10, history_y + 40 + i * 25))

    def update(self):
        # Обновление материального баланса
        self.calculate_material()

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
                piece = self.grid[self.prom_square[3]][self.prom_square[2]]
                move_notation = self.get_move_notation(piece, (self.prom_square[2], self.prom_square[3]), (self.prom_square[0], self.prom_square[1]),  self.prom_square[4])
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

                if self.color_to_move == 1:  # Белые
                    self.move_history.append(f"{self.move_number}. {move_notation}")
                else:  # Черные
                    if self.move_history and not self.move_history[-1].endswith(' '):
                        self.move_history[-1] += f" {move_notation}"
                        self.move_number += 1
                    else:
                        self.move_history.append(f"{self.move_number}... {move_notation}")
                        self.move_number += 1

                self.check_attacks()
                self.color_to_move = -self.color_to_move
                self.timer.switch_turn()
            self.prom_square = tuple()
            return
        if self.active_cell is not None:
            for i in (0, 1, 2, 3, 4, 5):
                if (clicked_cell[0], clicked_cell[1], i) in self.valid_moves:
                    piece = self.grid[self.active_cell[1]][self.active_cell[0]]
                    move_notation = self.get_move_notation(piece, self.active_cell, clicked_cell, i)

                    # Добавляем ход в историю
                    if self.color_to_move == 1:  # Белые
                        self.move_history.append(f"{self.move_number}. {move_notation}")
                    else:  # Черные
                        if self.move_history and not self.move_history[-1].endswith(' '):
                            self.move_history[-1] += f" {move_notation}"
                            self.move_number += 1
                        else:
                            self.move_history.append(f"{self.move_number}... {move_notation}")
                            self.move_number += 1

                    # Запоминаем съеденную фигуру
                    if i == 1:  # Взятие фигуры
                        captured_piece = self.grid[clicked_cell[1]][clicked_cell[0]]
                        piece_type = captured_piece.__class__.__name__
                        if self.color_to_move == 1:  # Белые съели фигуру
                            self.captured_by_white.append(piece_type)
                        else:  # Черные съели фигуру
                            self.captured_by_black.append(piece_type)
                        if sounds_loaded: capture_sound.play()
                    elif isinstance(piece, King) and abs(clicked_cell[0] - self.active_cell[0]) == 2:  # Рокировка
                        if sounds_loaded: castle_sound.play()
                    else:  # Обычный ход
                        if sounds_loaded: move_sound.play()
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
        self.timer.switch_turn()
        self.update_sprites() # Отрисовываем спрайты после хода
        self.calculate_material()

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

    def quit(self):
        """Остановка таймера при завершении игры"""
        self.timer.stop()
        pg.mixer.stop()