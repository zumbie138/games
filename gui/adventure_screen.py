from gui.ui import GuiBase
from gui.widgets import Text, Button, PlayerStatusDisplay, MonsterStatusDisplay

class AdventureScreen(GuiBase):
    MODE_ADVENTURE = 1
    MODE_BATTLE = 2
    def __init__(self, screen, screen_callback, app):
        super().__init__(screen, screen_callback, app)
        self.app = app
        self.current_mode = self.MODE_ADVENTURE
        self.life_button = None
        self.mana_button = None
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
        life_potion = self.app.game_core.itens_core.verify_life_potion()
        mana_potion = self.app.game_core.itens_core.verify_mana_potion()
        
        player_status = PlayerStatusDisplay(400, 100, 280, 200, game_core=self.app.game_core)
        monster_status = MonsterStatusDisplay(200, 100, 180, 200, game_core=self.app.game_core)
        text = Text(100, 50, 300, 50, 'Battle in progress!')
        stop_button = Button(300, 300, 150, 50, 'Stop Battle', 
               action=self.stop_battle)
        self.life_button = Button(50, 300, 50, 50, 'life potion',
                action=self.use_life_potion, condition_check=self.has_life_potion)
        self.mana_button = Button(50, 360, 50, 50, 'mana potion',
                action=self.use_mana_potion, condition_check=self.has_mana_potion)
        
        return [
            player_status, monster_status, text, stop_button, self.life_button, self.mana_button
        ]
    
    def use_life_potion(self):
        potion_name = self.app.game_core.itens_core.verify_life_potion()
        if potion_name:
            self.app.game_core.itens_core.drink_life_potion(potion_name)
            
    def use_mana_potion(self):
        potion_name = self.app.game_core.itens_core.verify_mana_potion()
        if potion_name:
            self.app.game_core.itens_core.drink_mana_potion(potion_name)
    
    def has_life_potion(self):
        return bool(self.app.game_core.itens_core.verify_life_potion())
        
    def has_mana_potion(self):
        return bool(self.app.game_core.itens_core.verify_mana_potion())
    
    def update(self):
        super().update()
        
        if self.life_button:
            self.life_button.update()
        if self.mana_button:
            self.mana_button.update()
    
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