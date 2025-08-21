from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay
from database import MessageLog

class CityScreen(GuiBase):
    def __init__(self, screen, change_screen_callback, app=None):
        super().__init__(screen, change_screen_callback)
        self.current_place = None
        self.place_widgets = {}
        self.app = app
        self.setup_ui()
    
    def setup_ui(self):
        tavern_btn = Button(
            100, 100, 150, 50, 
            'Tavern', action=lambda: self.city_state('tavern')
            )
        
        market_btn = Button(
            100, 200, 150, 50,
            'Market', action=lambda: self.city_state('market')
            )
        
        temple_btn = Button(
            100, 300, 150, 50, 
            'Temple', action=lambda: self.city_state('temple')
            )
        
        blacksmith_btn = Button(
            100, 400, 150, 50, 
            'Blacksmith', action=lambda: self.city_state('blacksmith')
            )
        
        return_btn = Button(
            600, 500, 150, 50, 'Return',
            action=lambda: self.change_screen('start_game')
        )
        
        
        self.widgets.extend([tavern_btn, market_btn,  temple_btn, blacksmith_btn, return_btn])

        self.init_places()
        
        
    def init_places(self):
        self.place_widgets = {
            'tavern': [
                Text(300, 50, 100, 50, 'Welcome to the tavern.'),
                Button(300, 200, 150, 50, 'Buy Drink',
                       action=lambda: MessageLog.add_message("You're drunk!!"))
            ],
            'market': [
                Text(300, 50, 100, 50,'You are in the market.'),
                Button(300, 200, 150, 50, 'Buy potion.',
                       action=lambda: MessageLog.add_message("You buy some potions!!"))
            ],
            'temple':[
                Text(300, 50, 100, 50,'The sacred temple.'),
                Button(300, 200, 150, 50, 'Pray',
                       action=lambda: MessageLog.add_message("The Gods blessed you!"))
            ],
            'blacksmith':[
                Text(300, 50, 100, 50,'You enter the blacksmith store.'),
                Button(300, 200, 150, 50, 'Craft Weapon',
                       action=lambda: MessageLog.add_message("The weapon its forged!"))
            ]
        }
        for place in self.place_widgets.values():
            for widget in place:
                widget.visible = False
        
    def city_state(self, place_text):
        if self.current_place:
            for widget in self.place_widgets[self.current_place]:
                widget.visible = False
                if widget in self.widgets:
                    self.widgets.remove(widget)
        
        self.current_place = place_text
        for widget in self.place_widgets[place_text]:
            widget.visible = True
            if widget not in self.widgets:
                self.widgets.append(widget)