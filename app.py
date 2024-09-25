from core.start_character import CharacterStarter

class AppMenus():
    def __init__(self):
        self.char_start = CharacterStarter()
        
    def initial_menu(self):
        print('Welcome to the game: DemoN ExoduS !!!')
        while True:
            choice = str(input('[ 1 ] - New Game.\n[ 2 ] - Load Game.\n[ 3 ] - Quit.\n'))
            if choice == '1':
                self.char_start.new_character()
                self.player_menu()
            elif choice == '2':
                self.load_choices()
                self.player_menu()
            elif choice == '3':
                break
            else:
                print('invalid choice.')
                
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