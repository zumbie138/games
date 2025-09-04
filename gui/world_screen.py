from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay

class WorldMap(GuiBase):
    def __init__(self, screen, change_screen_callback, app):
        super().__init__(screen, change_screen_callback)
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        df_places = self.app.game_core.tiers_df
        df_places = df_places.reset_index(drop=True)
        for i, row in df_places.iterrows():
            place_btn = Button(250, 30 + i*55, 200, 50, row['name'],
                               action=lambda t=row['tier']: self.change_tier(t),
                               enable=False)
            self.widgets.append(place_btn)
            if row['min level'] <= self.app.game_core.player.level:
                place_btn.enable = True
        return_button = Button(
            500, 500, 150, 50, 'Return',
            action=lambda: self.change_screen('start_game')
        )
        self.widgets.append(return_button)
    
    def change_tier(self, tier):
        self.change_screen('start_game')
        self.app.game_core.set_place_tier(tier)