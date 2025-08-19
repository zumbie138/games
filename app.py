import pygame
from gui import InitialScreen, NEWCHARscreen, LoadGameScreen, GamePlay, CityScreen, RefugeScreen, Journal
from core import GameCore
from graph import GraficMenus

class AppStatus():
    def __init__(self):
        #parametros de inicialização do pygame
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Demon Exodus')
        self.clock = pygame.time.Clock()
        
        #variaveis do app
        self.current_screen = None
        self.running = True
        self.fps = 60
        
        #atribuição das classes
        self.game_core = GameCore()
        self.graph_menu = GraficMenus()
        
        #inicia com a tela padrao
        self._init_journal()
        self.change_screen('initial_screen')
    
    def _init_journal(self):
        self.journal = Journal(
            x=0,
            y=450,
            width=600,
            height=150,
            max_lines=500,
        )
        self.journal.visible = False
        from database.game_repository import MessageLog
        MessageLog().journal = self.journal
        
    def enable_auto_journal(self):
        self.journal.visible = True
        if hasattr(self, 'journal_active'):
            del self.journal_active
    
    def disable_auto_journal(self):
        self.journal.visible = False
      
    def change_screen(self, screen_name, *args):
        screens = {
            'initial_screen': InitialScreen,
            'create_char':NEWCHARscreen,
            'load_char': LoadGameScreen,
            'start_game': GamePlay,
            'city_screen': CityScreen,
            'refuge_screen': RefugeScreen
        }
        if screen_name in ['start_game', 'city_screen', 'refuge_screen']: 
            self.enable_auto_journal()
        else:
            self.disable_auto_journal()
            
        if screen_name in screens:
            self.current_screen = screens[screen_name](self.screen, self.change_screen, self)
            
        if self.journal.visible and self.journal not in self.current_screen.widgets:
            self.current_screen.widgets.append(self.journal)    
        
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            for event in pygame.event.get():
                dt = clock.tick(60) / 1000
                
                if event.type == pygame.QUIT:
                    self.running = False
                    
                #delega eventos para tela atual
                if self.current_screen:
                    self.current_screen.handle_events(event)
            
            #da update e desenha widgets
            if self.current_screen:
                self.current_screen.update()
                self.current_screen.draw()
            
            pygame.display.flip()
            self.clock.tick(self.fps)
                        
    def pass_new_char_data(self, name, race, class_id):
        self.game_core.new_character_core(name, race, class_id)
    
    def list_load_character(self):
        return self.game_core.get_list_load_character()
    
    def run_load_character(self, save_choose):
        self.game_core.load_character_core(save_choose)
        
    # def run_game(self):
    #     start_menu = ['New Game.', 'Load Game.']
    #     start_text = '=+=+=+=+=+=+==+=+=+=+=+=+==+=+=+=+=+=+='
    #     self.graph_menu.starting_animation()
    #     while True:
    #         choice = self.graph_menu.generate_menu(start_text,start_menu)
    #         if int(choice) == len(start_menu) + 1:
    #             break
    #         match choice:
    #             case '1':
    #                 self.run_new_char()
    #             case '2':
    #                 self.run_load_character()
    #             case _:
    #                 print('invalid choice.')
    
    # def run_new_char(self):
    #     character = self.graph_menu.new_character_menu()
    #     self.game_core.new_character_core(*character)
    #     self.run_player_status()

        # while True:
        #     choice = int(self.graph_menu.generate_menu(text, save_list))
        #     if choice == len(save_list) + 1:
        #         break
        #     choice -= 1
        #     save_choose = save_list[choice]
        #     self.run_player_status()
        #     break
    
        
    # def run_player_status(self):
    #     choice_text = 'Welcome player, where you want to go?'
    #     choice_options = ['City.','Adventure.','Refuge.','World Map.']
    #     while True:
    #         self.game_core.save_character(self.game_core.player)
    #         choice = self.graph_menu.generate_menu(choice_text, choice_options)
    #         if int(choice) == len(choice_options)+1:
    #             break
    #         match choice:
    #             case '1':
    #                 self.run_city_status()
    #             case '2':
    #                 self.run_adventure_status()
    #             case '3':
    #                 self.run_refuge_status()
    #             case '4':
    #                 print('not yet')
    #             case _:
    #                 print('invalid choice.')
                    
    # def run_city_status(self):
    #     choice_text = 'You are inside the city, where you like to go?'
    #     choice_options = ['Tavern.','Market.','Temple.','Blacksmith.']
    #     while True:
    #         choice = self.graph_menu.generate_menu(choice_text, choice_options)
    #         if int(choice) == len(choice_options)+1:
    #             break
    #         match choice:
    #             case '1':
    #                 self.game_core.city_status_core('youre in tavern')
    #             case '2':
    #                 self.game_core.city_status_core('youre in market')
    #             case '3':
    #                 self.game_core.city_status_core('youre in temple')
    #             case '4':
    #                 self.game_core.city_status_core('youre in blacksmith')
    #             case _:
    #                 print('invalid choice.')

    def run_adventure_status(self):
        choice_text = 'Where you want to hunt?'
        loc_allowed = self.game_core.locations_allowed()
        while True:
            loc_choose = int(self.graph_menu.generate_menu(choice_text, loc_allowed))
            if loc_choose == len(loc_allowed) + 1:
                break
            loc_choose -= 1
            location = loc_allowed[loc_choose]
            self.game_core.battle_status_core(location)
        
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
                    self.game_core.show_character_core()
                case _:
                    print('invalid choice.')
    
    def run_wardobe_status(self):
        choice_text = 'What part you want to equip a item?'
        choice_text2 = 'What iten you want to equip ?'
        choice_options = ['head','neck','torso','arms','right hand','left hand','waist','legs','foot','finger','wrist','ears','back']
        while True:
            choice = int(self.graph_menu.generate_menu(choice_text,choice_options))
            if choice == len(choice_options)+1:
                break
            choice -= 1
            body_part_choose = choice_options[choice]
            wearable_list = self.game_core.itens_allowed(body_part_choose)
            wearable_list.append('Unequip')
            while True:
                iten_choice = int(self.graph_menu.generate_menu(choice_text2,wearable_list))
                if iten_choice == len(wearable_list):
                    self.game_core.manage_equips_core(False, '', body_part_choose) #True equip False unequip
                    break
                elif iten_choice == len(wearable_list)+1:
                    break
                iten_choice -= 1
                iten_choose = wearable_list[iten_choice]
                self.game_core.manage_equips_core(True, iten_choose, body_part_choose) #True equip False unequip
                break
            
    def run_sleep_status(self):
        self.game_core.healing_sleeping_core()           
             
    def run_train_status(self, train_choice):
        # choice_text = 'what skill do you want to train?'
        # choice_options = ['Strenght.','Agility.','Vitality.','intelligence.','charisma.']
        # while True:
        #     train_choice = self.graph_menu.generate_menu(choice_text,choice_options)
        #     if int(train_choice) == len(choice_options)+1:
        #         break
            self.game_core.training_core(train_choice)