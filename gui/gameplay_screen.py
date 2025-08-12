from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay

class GamePlay(GuiBase):
    def __init__(self, screen, change_screen_callback, app):
        super().__init__(screen, change_screen_callback)
        self.app = app
        self.setup_ui()
    
    def setup_ui(self):
        text = Text(100, 50, 100, 50,
                    'Welcome Player, what you want to do')
        
        char_display = PlayerStatusDisplay(
            400, 100, 280, 200,
            game_core=self.app.game_core
            )
        
        city_btn = Button(
            50, 100, 150, 50,
            'City', action= lambda: self.change_screen('city_screen')
            )
        
        refuge_btn = Button(
            50, 200, 150, 50, 
            'Refuge', action=  lambda: self.change_screen('refuge_screen')
            )
        
        world_btn = Button(
            50, 300, 150, 50, 
            'World map', action= lambda: self.change_screen('world_screen')
            )
        
        adventure_btn = Button(
            50, 400, 150, 50, 
            'Adventure', action= lambda: self.change_screen('adventure_screen')
            )
        
        return_button = Button(
            500, 500, 150, 50, 'Return',
            action=lambda: self.change_screen('initial_screen')
        )
        
        self.widgets.extend([text, char_display, city_btn, refuge_btn, world_btn, adventure_btn, return_button])