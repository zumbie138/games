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
                    self.run_player_status()
                case '2':
                    self.run_load_character()
                    self.run_player_status()
                case '3':
                    break
                case _:
                    print('invalid choice.')
    
    def run_new_char(self):
        character = self.graph_menu.new_character_menu()
        self.game_core.new_character(*character)
                
    def run_load_character(self):
        self.game_core.load_character()
        
    def run_player_status(self):
        while True:
            choice = self.graph_menu.player_menu()
            match choice:
                case '1':
                    self.run_city_status()
                case '2':
                    self.run_adventure_status()
                case '3':
                    self.run_refuge_status()
                case '4':
                    print('not yet')
                case '5':
                    break
                case _:
                    print('invalid choice.')
                    
    def run_city_status(self):
        city_choice = self.graph_menu.city_menu()
        print(city_choice)

    def run_adventure_status(self):
        loc_allowed = self.game_core.locations_allowed()
        loc_choose = self.graph_menu.adventure_menu(loc_allowed)
        self.game_core.monster_encounter(loc_choose)
    
    def run_refuge_status(self):
        while True:
            refuge_choice = self.graph_menu.refuge_menu()
            match refuge_choice:
                case '1':
                    self.run_sleep_status()
                case '2':
                    self.run_train_status()
                case '3':
                    print('not implemented yet')
                case '4':
                    self.game_core.show_character()
                case '5':
                    break
    def run_sleep_status(self):
        print('zzzzzzzzzz')            
             
    def run_train_status(self):
        while True:
            train_choice = self.graph_menu.train_skill_menu()
            match train_choice:
                case '1':
                    print('up strength')
                case '2':
                    print('up agility')
                case '3':
                    print('up vitality')
                case '4':
                    print('up intelligence')        
                case '5':
                    print('up charisma')
                case '6':
                    break    