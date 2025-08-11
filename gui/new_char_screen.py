from gui.ui import GuiBase
from gui.widgets import Button, TextInput

class NEWCHARscreen(GuiBase):
    def __init__(self, screen, screen_callback, app):
        super().__init__(screen, screen_callback)
        self.app = app
        self.class_select = {
            'human':{'1':'warrior','2':'wizard','3':'cleric'},
            'elf':{'1':'ranger','2':'sorcerer','3':'druid'},
            'orc':{'1':'barbarian','2':'witch','3':'shaman'}
        }
        self.selected_race = None
        self.selected_class = None
        self.player_name = ''
        self.setup_ui()
    
    def setup_ui(self):
        self.name_input = TextInput(
            x=100, y=50, width=300, height=40,
            placeholder='Character name',
            on_change=lambda text: setattr(self, 'player_name', text)
        )
        
        self.race_button = [
            Button(100, 120, 120, 120, 'Human',
                   action=lambda: self.select_race('human')),
            Button(250, 120, 120, 120, 'Elf',
                   action=lambda: self.select_race('elf')),
            Button(400, 120, 120, 120, 'Orc',
                   action=lambda: self.select_race('orc')),
        ]
        
        self.class_button =[]
        
        self.confirm_button = Button(
            300, 400, 200, 50, 'Start adventure',
            action=self.start_game,
            enable=False
        )
        
        self.back_button = Button(
            x=100, y=400, width=150, height=50, text='Return',
            action=lambda: self.change_screen('initial_screen')
        )
        
        self.widgets = [self.name_input, *self.race_button, self.confirm_button, self.back_button]
        
        
    def select_race(self, race):
        self.selected_race = race
        self.selected_class = None
        self.update_class_buttons()
        self.check_confirmation()
    
    def select_class(self, class_id):
        self.selected_class = self.class_select[self.selected_race][class_id]
        self.check_confirmation()
        
    def update_class_buttons(self):
        for btn in self.class_button:
            if btn in self.widgets:
                self.widgets.remove(btn)
        
        self.class_button = []
        if self.selected_race:
            classes = self.class_select[self.selected_race]
            for i, (key, cls) in enumerate(classes.items()):
                btn = Button(
                    100 + i*150, 280, 140, 40, cls.capitalize(),
                    action=lambda k=key: self.select_class(k)
                )
                self.class_button.append(btn)
                self.widgets.append(btn)
    
    def check_confirmation(self):
        all_filled = (self.player_name and
                      self.selected_race and
                      self.selected_class)
        self.confirm_button.enable = all_filled
        
    def start_game(self):
        self.app.pass_new_char_data(self.player_name, self.selected_race, self.selected_class)
        self.change_screen('start_game')