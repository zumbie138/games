from gui.ui import GuiBase
from gui.widgets import Button

class LoadGameScreen(GuiBase):
    def __init__(self, screen, change_screen_callback, app):
        super().__init__(screen, change_screen_callback)
        self.app = app
        self.load_button = []
        self.selected_load = None
        self.setup_ui()
        
    def setup_ui(self):
        save_list = self.app.list_load_character()
        for i, save in enumerate(save_list):
            btn = Button(
                300, 100 + i*50, 140, 40, save.strip('.json'),
                action=lambda s=save:self.start_game(s)
            )
            self.load_button.append(btn)
            self.widgets.append(btn)

        return_button = Button(
            500, 500, 150, 50, 'Return',
            action=lambda: self.change_screen('initial_screen')
        )
        self.widgets.append(return_button)
        
    def start_game(self,save_choose):
        self.app.run_load_character(save_choose)
        self.change_screen('start_game', self.app)
        