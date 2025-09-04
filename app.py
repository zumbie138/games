import pygame
from gui import InitialScreen, NEWCHARscreen, LoadGameScreen, GamePlay, CityScreen, RefugeScreen, Journal, AdventureScreen, WorldMap
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
        self.game_core.start_menu_state()
        screens = {
            'initial_screen': InitialScreen,
            'create_char':NEWCHARscreen,
            'load_char': LoadGameScreen,
            'start_game': GamePlay,
            'city_screen': CityScreen,
            'refuge_screen': RefugeScreen,
            'adventure_screen': AdventureScreen,
            'world_screen': WorldMap
        }
        if screen_name in ['initial_screen', 'create_char', 'load_char']:
            self.disable_auto_journal()
        else:
            self.enable_auto_journal()
            
        if screen_name in screens:
            self.current_screen = screens[screen_name](self.screen, self.change_screen, self)
            
        if self.journal.visible and self.journal not in self.current_screen.widgets:
            self.current_screen.widgets.append(self.journal)    
        
    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(60) / 1000
            self.game_core.update_states(dt)
            
            for event in pygame.event.get():
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

    def run_sleep_status(self):
        self.game_core.start_healing_sleeping()

    def run_train_status(self, train_choice):
        self.game_core.start_training(train_choice)
        