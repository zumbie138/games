from core.start_character import CharacterStarter

class AppMenus():
    def __init__(self):
        self.char_start = CharacterStarter()
        
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
        class_select={'Humano':{'1':'guerreiro','2':'mago','3':'clerigo'},
                'Elfo':{'1':'ranger','2':'feiticeiro','3':'druida'},
                'Orc':{'1':'barbaro','2':'bruxo','3':'shaman'}}
        race_select={'1':'Humano','2':'Elfo','3':'Orc'}
        print('!!TELA DE CRIAÇÃO DE PERSONAGEM!!')
        name = str(input('Coloque o nome do seu personagem: '))
        race_choice = str(input('Escolha sua raça: \n [ 1 ] - Humano.\n [ 2 ] - Elfo.\n [ 3 ] - Orc.\n'))
        choosen_race = race_select[race_choice]
        class_choice = str(input(f'Escolha sua classe: \n [ 1 ] - {class_select[choosen_race]["1"].title()}.\n [ 2 ] - {class_select[choosen_race]["2"].title()}.\n [ 3 ] - {class_select[choosen_race]["3"].title()}.\n'))
        choosen_class = class_select[choosen_race][class_choice]
        self.char_start.new_character(name,choosen_race, choosen_class)
                
    def load_choices(self):
        self.char_start.saved_character()
        
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