from UI_Engine import *
from Game import Board
from functools import partial

from fontTools.merge import timer


class Game:
    def __init__(self):
        self.current_options = {
            "player_one": 1, # 1 - White, -1 - Black
            "timer": 300,
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
        def play_2_players():
            self.current_widget = "game"
            self.board = Board(self, self.current_options["player_one"], self.current_options["timer"], (150, 50), 70)

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
            Button(self.MainMenu, (490, 180), size=(300, 50), text="Play", action=play_2_players))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 260), size=(300, 50), text="Options", action=options))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 340), size=(300, 50), text="Quit", action=quit))

        def main_menu():
            self.current_widget = "main"

        def set_time_limit(time, timer_text):
            timer_text.text = "Minutes: " + str(time // 60)
            self.current_options["timer"] = time

        def set_player_one(color, color_text):
            color_text.text = {1: "White", -1: "Black"}[color]
            self.current_options["player_one"] = color

        def resign():
            if not self.board.game_condition:
                if self.board.color_to_move == 1:
                    self.board.move_history += ["0 - 1"]
                    self.board.game_condition = -1
                    self.board.quit()
                    print("Black won by resignation")
                elif self.board.color_to_move == -1:
                    self.board.move_history += ["1 - 0"]
                    self.board.game_condition = 1
                    self.board.quit()
                    print("White won by resignation")

        def draw():
            if not self.board.game_condition:
                self.board.move_history += ["0.5 - 0.5"]
                self.board.game_condition = 0.5
                print("Draw by agreement")

        timer_text = Text((50, 250), text="Minutes: 5", font_size=40)
        color_text = Text((50, 400), text="White", font_size=40)
        self.OptionsMenu = Widget(self, [], [
            Text((570, 30), "Options", None, 48),
        ])
        self.OptionsMenu.add_button(
            Button(self.OptionsMenu, (490, 100), size=(300, 50), text="Back to Main Menu", action=main_menu))
        self.OptionsMenu.add_text(Text((50, 200), text="Time limit", font_size=40))
        self.OptionsMenu.add_text(Text((50, 350), text="Player one color", font_size=40))
        self.OptionsMenu.add_text(Text((50, 600), text="To (un)mute music, press Spacebar!", font_size=40))
        self.OptionsMenu.add_text(timer_text)
        self.OptionsMenu.add_text(color_text)
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (300, 190), size=(100, 50), text="1:00", action=partial(set_time_limit, 60, timer_text)))
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (500, 190), size=(100, 50), text="3:00", action=partial(set_time_limit, 180, timer_text)))
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (700, 190), size=(100, 50), text="5:00", action=partial(set_time_limit, 300, timer_text)))
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (900, 190), size=(100, 50), text="10:00", action=partial(set_time_limit, 600, timer_text)))
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (1100, 190), size=(100, 50), text="30:00", action=partial(set_time_limit, 1800, timer_text)))
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (350, 340), size=(100, 50), text="White", action=partial(set_player_one, 1, color_text)))
        self.OptionsMenu.add_button(Button(
            self.OptionsMenu, (550, 340), size=(100, 50), text="Black", action=partial(set_player_one, -1, color_text)))

        self.GameMenu = Widget(self, [], [])
        self.GameMenu.add_button(Button(self.GameMenu, (20, 20), size=(100, 40), text="Leave", action=leave_game))
        self.GameMenu.add_button(Button(self.GameMenu, (120, 270), size=(200, 40), text="Resign", action=resign))
        self.GameMenu.add_button(Button(self.GameMenu, (120, 350), size=(200, 40), text="Draw", action=draw))

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
