# ChessTimer.py
import pygame as pg
import time
import threading

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

    def start_game(self, starting_player="white"):
        self.reset()
        self.active_player = 1 if starting_player == "white" else 2

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
        surface.blit(time_text, (rect.centerx - time_text.get_width()//2, 
                                rect.centery - time_text.get_height()//2))
        
        # Подпись
        label = self.font_small.render("     ", True, self.INFO_COLOR)
        surface.blit(label, (rect.centerx - label.get_width()//2, 
                            rect.top + 10))

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
        surface.blit(time_text, (rect.centerx - time_text.get_width()//2, 
                                rect.centery - time_text.get_height()//2))
        
        # Подпись
        label = self.font_small.render("      ", True, self.INFO_COLOR)
        surface.blit(label, (rect.centerx - label.get_width()//2, 
                            rect.top + 10))
    
    def stop(self):
        """Остановка таймера при завершении игры"""
        self.running = False