from gui.ui import GuiBase
from gui.widgets import Text, Button, PlayerStatusDisplay, MonsterStatusDisplay

class AdventureScreen(GuiBase):
    MODE_ADVENTURE = 1
    MODE_BATTLE = 2
    def __init__(self, screen, screen_callback, app):
        super().__init__(screen, screen_callback, app)
        self.app = app
        self.current_mode = self.MODE_ADVENTURE
        self.setup_ui()
    
    def setup_ui(self):
        self.adventure_widgets = self._create_adventure_ui()
        self.battle_widgets = self._crerate_battle_ui()
        
        self.widgets = self.adventure_widgets.copy()
        
    def _create_adventure_ui(self):
        
        widgets = [
            Text(100, 50, 100, 50,'where do you want to adventure'),
            PlayerStatusDisplay(400, 100, 280, 200,game_core=self.app.game_core),
            Button(600, 500, 150, 50, 'Return',action=lambda: self.change_screen('start_game'))
        ]
        loc_allowed = self.app.game_core.locations_allowed()
        loc_allowed = loc_allowed.reset_index(drop=True)
        
        for i, location in loc_allowed.iterrows():
            btn = Button(
                200, 100 + i*60, 150, 50,
                location['name'], action=lambda l=location['name']: self.start_battle(l),
                enable=False
                )
            widgets.append(btn)
            if location['min lvl'] <= self.app.game_core.player.level:
                btn.enable = True
            
            
        return widgets
    
    def _crerate_battle_ui(self):
        return [
            PlayerStatusDisplay(400, 100, 280, 200, game_core=self.app.game_core),
            Text(100, 50, 300, 50, 'Battle in progress!'),
            Button(300, 300, 150, 50, 'Stop Battle', 
               action=self.stop_battle),
            MonsterStatusDisplay(200, 100, 180, 200, game_core=self.app.game_core)
        ]
    
    def start_battle(self, location):
        self.current_mode = self.MODE_BATTLE
        self._switch_widgets(self.battle_widgets)
        
        self.app.game_core.start_battle(location)
        
    def stop_battle(self):
        self.current_mode = self.MODE_ADVENTURE
        self._switch_widgets(self.adventure_widgets)
        
        self.app.game_core.stop_battle()
        
    def _switch_widgets(self, new_widgets):
        self.widgets = new_widgets.copy()

        if (hasattr(self.app, 'journal') and 
            self.app.journal.visible and 
            self.app.journal not in self.widgets):
            
            self.widgets.append(self.app.journal)