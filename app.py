from core import GameCore
from graph import GraficMenus
import keyboard

class AppMenus():
    def __init__(self):
        self.game_core = GameCore()
        self.graph_menu = GraficMenus()
        
    def run_game(self):
        start_menu = ['New Game.', 'Load Game.']
        start_text = '=+=+=+=+=+=+==+=+=+=+=+=+==+=+=+=+=+=+='
        self.graph_menu.starting_animation()
        while True:
            choice = self.graph_menu.generate_menu(start_text,start_menu)
            if int(choice) == len(start_menu) + 1:
                break
            match choice:
                case '1':
                    self.run_new_char()
                    self.run_player_status()
                case '2':
                    self.run_load_character()
                case _:
                    print('invalid choice.')
    
    def run_new_char(self):
        character = self.graph_menu.new_character_menu()
        self.game_core.new_character(*character)
                
    def run_load_character(self):
        text = 'What character want to load?'
        save_list = self.game_core.get_list_load_character()
        while True:
            choice = int(self.graph_menu.generate_menu(text, save_list))
            if choice == len(save_list) + 1:
                break
            choice -= 1
            char_data = self.game_core.get_char_from_json(save_list[choice])
            self.game_core.load_character(char_data)
            self.run_player_status()
            break
        
    def run_player_status(self):
        choice_text = 'Welcome player, where you want to go?'
        choice_options = ['City.','Adventure.','Refuge.','World Map.']
        while True:
            self.game_core.save_character(self.game_core.player)
            choice = self.graph_menu.generate_menu(choice_text, choice_options)
            if int(choice) == len(choice_options)+1:
                break
            match choice:
                case '1':
                    self.run_city_status()
                case '2':
                    self.run_adventure_status()
                case '3':
                    self.run_refuge_status()
                case '4':
                    print('not yet')
                case _:
                    print('invalid choice.')
                    
    def run_city_status(self):
        choice_text = 'You are inside the city, where you like to go?'
        choice_options = ['Tavern.','Market.','Temple.','Blacksmith.']
        while True:
            choice = self.graph_menu.generate_menu(choice_text, choice_options)
            if int(choice) == len(choice_options)+1:
                break
            match choice:
                case '1':
                    print('youre in tavern')
                case '2':
                    print('youre in market')
                case '3':
                    print('youre in temple')
                case '4':
                    print('youre in blacksmith')
                case _:
                    print('invalid choice.')

    def run_adventure_status(self):
        choice_text = 'Where you want to hunt?'
        loc_allowed = self.game_core.locations_allowed()
        while True:
            loc_choose = int(self.graph_menu.generate_menu(choice_text, loc_allowed))
            if loc_choose == len(loc_allowed) + 1:
                break
            loc_choose -= 1
            stop_battle = False
            while not stop_battle:
                self.game_core.monster_encounter(loc_allowed[loc_choose])
                stop_battle = self.game_core.battle_core()
        
    def run_refuge_status(self):
        choice_text = 'Welcome to your home. What do you wish to do?'
        choice_options = ['Sleep in bed.','Train.','Wardobe.','look in to the mirror.']
        while True:
            refuge_choice = self.graph_menu.generate_menu(choice_text,choice_options)
            if int(refuge_choice) == len(choice_options)+1:
                break
            match refuge_choice:
                case '1':
                    self.run_sleep_status()
                case '2':
                    self.run_train_status()
                case '3':
                    self.run_wardobe_status()
                case '4':
                    self.game_core.show_character()
                case _:
                    print('invalid choice.')
    
    def run_wardobe_status(self):
        choice_text = 'What part you want to equip a item?'
        choice_text2 = 'What inten you want to equip ?'
        choice_options = ['head','neck','torso','arms','right hand','left hand','waist','legs','foot','finger','wrist','ears','back']
        while True:
            choice = int(self.graph_menu.generate_menu(choice_text,choice_options))
            if choice == len(choice_options)+1:
                break
            choice -= 1
            body_part_choose = choice_options[choice]
            wearable_list = self.game_core.list_wering_equipment(body_part_choose)
            while True:
                iten_choice = int(self.graph_menu.generate_menu(choice_text2,wearable_list))
                if iten_choice == len(wearable_list)+1:
                    break
                iten_choice -= 1
                iten_choose = wearable_list[iten_choice]
                self.game_core.equip_item(iten_choose, body_part_choose)
                break
            
    def run_sleep_status(self):
        self.game_core.healing_sleeping()           
             
    def run_train_status(self):
        choice_text = 'what skill do you want to train?'
        choice_options = ['Strenght.','Agility.','Vitality.','intelligence.','charisma.']
        while True:
            train_choice = self.graph_menu.generate_menu(choice_text,choice_options)
            if int(train_choice) == len(choice_options)+1:
                break
            self.game_core.training_atributes(train_choice)