from core.game_core import GameCore

class AppMenus():
    def __init__(self):
        self.game_core = GameCore()
        
    def initial_menu(self):
        print('Welcome to the game: DemoN ExoduS !!!')
        while True:
            choice = str(input('[ 1 ] - New Game.\n[ 2 ] - Load Game.\n[ 3 ] - Quit.\n'))
            if choice == '1':
                self.new_char_menu()
                self.player_menu()
            elif choice == '2':
                self.load_choices()
                self.player_menu()
            elif choice == '3':
                break
            else:
                print('invalid choice.')
    
    def new_char_menu(self):
        class_select={'human':{'1':'warrior','2':'wizard','3':'cleric'},
                'elf':{'1':'ranger','2':'sorcerer','3':'druid'},
                'orc':{'1':'barbarian','2':'witch','3':'shaman'}}
        race_select={'1':'human','2':'elf','3':'orc'}
        print('!!CHARACTER CREATION!!')
        name = str(input('Character name: '))
        race_choice = str(input('Choose your race: \n [ 1 ] - Human.\n [ 2 ] - Elf.\n [ 3 ] - Orc.\n'))
        choosen_race = race_select[race_choice]
        class_choice = str(input(f'Choose your class: \n [ 1 ] - {class_select[choosen_race]["1"].title()}.\n [ 2 ] - {class_select[choosen_race]["2"].title()}.\n [ 3 ] - {class_select[choosen_race]["3"].title()}.\n'))
        choosen_class = class_select[choosen_race][class_choice]
        self.game_core.new_character(name,choosen_race, choosen_class)
                
    def load_choices(self):
        self.game_core.saved_character()
        
    def player_menu(self):
        print('Welcome player')
        while True:
            choice = str(input('[ 1 ] - Cidade.\n[ 2 ] - Aventura.\n[ 3 ] - Refúgio.\n[ 4 ] - Sair.'))
            if choice == '1':
                self.city_menu()
            elif choice == '2':
                self.adventure_menu()
            elif choice == '3':
                print('Youre home')
            elif choice == '4':
                break
            else:
                print('Invalid choice.')
    def city_menu(self):
        print('Welcome to the city')
    def adventure_menu(self):
        print('Where you want to hunt?')