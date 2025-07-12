import datetime
import json
import pygame as pg
from UI_Engine import *
from Board import Board
from random import randint


class Game:
    def __init__(self):
        self.current_options = {
            "mode": "2 players",
            "player_one": 1, # 1 - White, -1 - Black
            "timer": -1,
        }

        self.any_widget_active = True
        self.current_widget = "main"

        self.running = True
        self.init_widgets()

        pg.init()
        pg.mixer.init()
        self.size = self.width, self.height = 1260, 720
        self.screen = pg.display.set_mode(self.size, pg.DOUBLEBUF)
        self.screen.set_alpha(None)

        self.board = None

    def init_widgets(self):
        def play_with_bot():
            pass

        def play_2_players():
            self.current_widget = "game"
            self.board = Board(self, self.current_options["player_one"], (150, 50), 70)

        def options():
            self.current_widget = "options"

        def quit():
            self.running = False

        def leave_game():
            if self.board:
                self.board.quit()
            self.current_widget = "main"

        self.MainMenu = Widget(self, [], [
            Text((585, 30), "Chess", None, 48)
        ])
        self.MainMenu.add_button(
            Button(self.MainMenu, (490, 100), size=(300, 50), text="Play with Bot", action=play_with_bot))
        self.MainMenu.add_button(
            Button(self.MainMenu, (490, 180), size=(300, 50), text="Play 2 Players", action=play_2_players))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 260), size=(300, 50), text="Options", action=options))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 340), size=(300, 50), text="Quit", action=quit))

        def main_menu():
            self.current_widget = "main"

        self.OptionsMenu = Widget(self, [], [
            Text((570, 30), "Options", None, 48),
        ])
        self.OptionsMenu.add_button(
            Button(self.OptionsMenu, (490, 100), size=(300, 50), text="Back to Main Menu", action=main_menu))

        self.GameMenu = Widget(self, [], [])
        self.GameMenu.add_button(Button(self.GameMenu, (20, 20), size=(100, 40), text="Leave", action=leave_game))

        self.widgets = {
            "main": self.MainMenu,
            "options": self.OptionsMenu,
            "game": self.GameMenu
        }

    def render_screen(self):
        if self.any_widget_active:
            current_widget = self.widgets[self.current_widget]

            if self.current_widget == "game" and self.board:
                self.board.render(self.screen)

            current_widget.render(self.screen)

    def run_game(self):
        pg.display.set_icon(pg.image.load("Assets/Images/icon.png"))
        pg.display.set_caption("Chess")
        max_fps = 60
        clock = pg.time.Clock()

        try:
            pg.mixer.music.load("Assets/sounds/bg.mp3")
            pg.mixer.music.set_volume(0.3)
            pg.mixer.music.play(-1)
            music_loaded = True
        except:
            music_loaded = False

        while self.running:
            self.screen.fill((40, 40, 40))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    if self.board:
                        self.board.quit()
                    self.running = False

                if self.any_widget_active:
                    current_widget = self.widgets[self.current_widget]
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        if self.current_widget == "game" and self.board:
                            self.board.get_click(event.pos)
                        current_widget.get_click(event.pos)
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE and music_loaded:
                            if pg.mixer.music.get_busy():
                                pg.mixer.music.pause()
                            else:
                                pg.mixer.music.unpause()
                else:
                    pass

            self.render_screen()
            clock.tick(max_fps)
            pg.display.flip()

        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()
