
class GraficMenus():
    def starting_animation(self):
        print('=+=+=+=+=+=+= DEMON EXODUS =+=+=+=+=+=+=')

          
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
    
    
    def generate_menu(self,menu_text:str,options:list)->str:
        print(menu_text) 
        for index, option in enumerate(options):
            print(f'[ {index+1} ] - {option}')
        print(f'[ {len(options) + 1} ] - Exit.')
        while True:
            choice = str(input('Choose a option:\n'))
            if choice.isnumeric():
                if 1 <= int(choice) <= len(options)+1:
                    return choice
                
    def worldmap_menu(self):
        print('Not working yet.')