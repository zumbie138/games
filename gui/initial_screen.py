from gui.ui import GuiBase
from gui.widgets import Button

class InitialScreen(GuiBase):
    def __init__(self, screen, screen_callback, app):
        super().__init__(screen, screen_callback)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        btn_create = Button(
            x=100, y=100, width=200, height=50,
            text='New Game',
            action=lambda: self.change_screen('create_char')
        )
        
        btn_load = Button(
            x=100, y=200, width=200, height=50,
            text='Load Game',
            action=lambda:  self.change_screen('load_char')
            )
        
        btn_quit = Button(
            x=100, y=300, width=200, height=50,
            text='Exit Game',
            action=lambda: setattr(self.app, 'running', False)
        )
        
        self.widgets.extend([btn_create, btn_load, btn_quit])