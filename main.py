import datetime
import json
from UI_Engine import *
from Board import Piece, Board
from random import randint

class Game:
    def __init__(self):

        self.current_options = {
            "mode": "2 players",
            "first_player": "white",
            "timer": -1,
        }
        
        self.any_widget_active = True
        self.current_widget = "main"
        
        self.running = True
        self.init_widgets()

        pg.init()
        # pg.mixer.init()
        # pg.mixer.music.set_endevent(pg.USEREVENT + 1)
        self.size = self.width, self.height = 1280, 720
        self.screen = pg.display.set_mode(self.size, pg.DOUBLEBUF)
        self.screen.set_alpha(None)

        self.board = None
    
    def init_widgets(self):
        def play_with_bot():
            pass
        def play_2_players():
            self.current_widget = "game"
            self.board = Board(self, self.current_options["first_player"], (300, 20), 85)
        def options():
            self.current_widget = "options"
        def quit():
            self.running = False
            
        self.MainMenu = Widget(self, [], [
            Text((585, 30), "Chess", None, 48)
        ])
        self.MainMenu.add_button(Button(self.MainMenu, (490, 100), size=(300, 50), text="Play with Bot", action=play_with_bot))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 180), size=(300, 50), text="Play 2 Players", action=play_2_players))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 260), size=(300, 50), text="Options", action=options))
        self.MainMenu.add_button(Button(self.MainMenu, (490, 340), size=(300, 50), text="Quit", action=quit))

        def main_menu():
            self.current_widget = "main"

        self.OptionsMenu = Widget(self, [], [
            Text((570, 30), "Options", None, 48),
        ])
        self.OptionsMenu.add_button(Button(self.OptionsMenu, (490, 100), size=(300, 50), text="Back to Main Menu", action=main_menu))

        self.GameMenu = Widget(self, [], [])

        self.GameMenu.add_button(Button(self.GameMenu, (20, 20), size=(100, 40), text="Leave", action=main_menu))

        self.widgets = {
            "main": self.MainMenu,
            "options": self.OptionsMenu,
            "game": self.GameMenu
        }

    def render_screen(self):
        if self.any_widget_active:
            current_widget = self.widgets[self.current_widget]

            current_widget.render(self.screen)
            if self.current_widget == "game":
                self.board.render(self.screen)
        else:
            pass
    
    def run_game(self):
        
        pg.display.set_icon(pg.image.load("Assets/Images/icon.png"))
        pg.display.set_caption("Chess")
        max_fps = 30
        screen = self.screen
        clock = pg.time.Clock()
        # pg.mixer.music.load("Assets/Sounds/music.mp3")
        # pg.mixer.music.set_volume(0.1)
        # pg.mixer.music.play()

        # txt_color = (255, 255, 255)
        # txt_font = pg.font.Font(None, 32)
        # txt_pos = (1, 1)

        while self.running:
            screen.fill(pg.Color(40, 40, 40))

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                # if event.type == pg.USEREVENT + 1:
                #     pg.mixer.music.play()
                if self.any_widget_active:
                    current_widget = self.widgets[self.current_widget]
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                        current_widget.get_click(event.pos)
                    if event.type == pg.MOUSEMOTION:
                        current_widget.get_motion(event.pos)
                else:
                    pass

            self.render_screen()

            clock.tick(max_fps)

            pg.display.flip()
        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()
