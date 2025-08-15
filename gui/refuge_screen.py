from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay

class RefugeScreen(GuiBase):
    def __init__(self, screen, change_screen_callback, app=None):
        super().__init__(screen, change_screen_callback)
        self.current_object = False
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        
        refuge_text = Text(
                100, 50, 100, 50,
                'Welcome to your house, what you want to do'
                )
        player_display = PlayerStatusDisplay(
                400, 100, 280, 200,
                game_core=self.app.game_core
            )
        bed_btn = Button(
                100, 100, 150, 50, 'Sleep in bed',
                action=lambda: self.app.run_sleep_status()
            )
        train_btn = Button(
                100, 200, 150, 50, 'Train',
                action=lambda: self.refuge_state()
            )
        wardobe_btn = Button(
                100, 300, 150, 50, 'Wardobe',
                action=lambda: self.app.run_wardobe_status()
            )
        mirror_btn = Button(
                100, 400, 150, 50, 'Mirror',
                action=lambda: self.app.game_core.show_character_core()
            )
        return_btn = Button(
                500, 500, 150, 50, 'Return',
                action=lambda: self.change_screen('start_game')
            )
        
        self.widgets.extend([refuge_text, player_display, bed_btn, train_btn, wardobe_btn, mirror_btn, return_btn])
        self.init_training_objects()
        
        
    def init_training_objects(self):
        self.object_widgets = [
            Button(
                260, 100, 100, 40, 'Strenght.',
                action=lambda: self.app.run_train_status('strength')
                ),
            Button(
                260, 150, 100, 40, 'Agility.',
                action=lambda: self.app.run_train_status('agility')
                ),
            Button(
                260, 200, 100, 40, 'Vitality.',
                action=lambda: self.app.run_train_status('vitality')
                ),
            Button(
                260, 250, 100, 40, 'Intelligence.',
                action=lambda: self.app.run_train_status('intelligence')
                ),
            Button(
                260, 300, 100, 40, 'Charisma.',
                action=lambda: self.app.run_train_status('charisma')
                ),
        ]
        for widget in self.object_widgets:
            widget.visible = False
        
    def refuge_state(self):
        if self.current_object:
            for widget in self.object_widgets:
                widget.visible = False
        self.current_object = True
        
        for widget in self.object_widgets:
            widget.visible = True 
            if widget not in self.widgets:
                self.widgets.append(widget)
        