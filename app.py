from core import GameCore
from graph import GraficMenus
import keyboard

class AppMenus():
    def __init__(self):
        self.game_core = GameCore()
        self.graph_menu = GraficMenus()
        
    def run_game(self):
        start_menu = ['New Game.', 'Load Game.', 'Exit.']
        start_text = '=+=+=+=+=+=+==+=+=+=+=+=+==+=+=+=+=+=+='
        self.graph_menu.starting_animation()
        while True:
            choice = self.graph_menu.generate_menu(start_text,start_menu)
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
        choice_text = 'Welcome player, where you want to go?'
        choice_options = ['City.','Adventure.','Refuge.','World Map.','Exit.']
        while True:
            choice = self.graph_menu.generate_menu(choice_text, choice_options)
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
        choice_text = 'You are inside the city, where you like to go?'
        choice_options = ['Tavern.','Market.','Temple.','Blacksmith.','Exit.']
        while True:
            choice = self.graph_menu.generate_menu(choice_text, choice_options)
            match choice:
                case '1':
                    print('youre in tavern')
                case '2':
                    print('youre in market')
                case '3':
                    print('youre in temple')
                case '4':
                    print('youre in blacksmith')
                case '5':
                    break
                case _:
                    print('invalid choice.')

    def run_adventure_status(self):
        choice_text = 'Where you want to hunt?'
        loc_allowed = self.game_core.locations_allowed()
        loc_choose = self.graph_menu.generate_menu(choice_text, loc_allowed)
        loc_choose = int(loc_choose)-1
        stop_battle = False
        while not stop_battle:
            self.game_core.monster_encounter(loc_allowed[loc_choose])
            stop_battle = self.game_core.battle_core()
    
    def run_refuge_status(self):
        choice_text = 'Welcome to your home. What do you wish to do?'
        choice_options = ['Sleep in bed.','Train.','Wardobe.','look in to the mirror.','Exit house..']
        while True:
            refuge_choice = self.graph_menu.generate_menu(choice_text,choice_options)
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
        choice_text = 'what skill do you want to train?'
        choice_options = ['Strenght.','Agility.','Vitality.','intelligence.','charisma.','Exit.']
        while True:
            train_choice = self.graph_menu.generate_menu(choice_text,choice_options)
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