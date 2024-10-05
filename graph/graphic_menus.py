
class GraficMenus():
    def starting_animation(self):
        print('Welcome to the game Demon Exodus')
        
    def initial_menu(self)->str:
        while True:
            choice = str(input('[ 1 ] - New Game.\n[ 2 ] - Load Game.\n[ 3 ] - Quit.\n'))
            if choice.isnumeric(): 
                if 1 <= int(choice) <= 3:
                    return choice
                else:
                    print('invalid choice.')                    
            else:
                print('invalid choice.')
    
    def new_character_menu(self)->tuple:
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
        return (name, choosen_race, choosen_class)
    
    def player_menu(self)->str:
        print('Welcome player')
        while True:
            choice = str(input('[ 1 ] - City.\n[ 2 ] - Adventure.\n[ 3 ] - Refugee.\n[ 4 ] - World Map.\n[ 5 ] - Exit.'))
            if choice.isnumeric():
                if 1 <= int(choice) <= 5:
                    return choice
                else:
                    print('Invalid choice.')
            else:
                print('Invalid choice.')
                
    def city_menu(self)->str:
        while True:
            choice = str(input('[ 1 ] - Tavern.\n[ 2 ] - Market.\n[ 3 ] - Temple.\n[ 4 ] - Blacksmith.\n[ 5 ] - Exit.'))
            if choice.isnumeric():
                if 1 <= int(choice) <= 5:
                    return choice
                else:
                    print('Invalid choice.')
            else:
                print('Invalid choice.')
                
    def worldmap_menu(self):
        print('Not working yet.')