from core import GameCore
from graph import GraficMenus

class AppMenus():
    def __init__(self):
        self.game_core = GameCore()
        self.graph_menu = GraficMenus()
        
    def run_game(self):
        self.graph_menu.starting_animation()
        while True:
            choice = self.graph_menu.initial_menu()
            match choice:
                case '1':
                    self.run_new_char()
                    self.run_player_menu()
                case '2':
                    self.run_load_character()
                    self.run_player_menu()
                case '3':
                    break
                case _:
                    print('invalid choice.')
    
    def run_new_char(self):
        character = self.graph_menu.new_character_menu()
        self.game_core.new_character(*character)
                
    def run_load_character(self):
        self.game_core.load_character()
        
    def run_player_menu(self):
        while True:
            choice = self.graph_menu.player_menu()
            match choice:
                case '1':
                    self.run_city_menu()
                case '2':
                    self.run_adventure_menu()
                case '3':
                    print('Youre home')
                    self.game_core.show_character()
                case '4':
                    print('not yet')
                case '5':
                    break
                case _:
                    print('invalid choice.')
                    
    def run_city_menu(self):
        print('Welcome to the city')

    def run_adventure_menu(self):
        print('Where you want to hunt?')
        