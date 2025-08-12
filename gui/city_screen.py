from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay

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
            'Tavern', action=lambda: self.city_state('Welcome to the tavern.')
            )
        
        market_btn = Button(
            100, 200, 150, 50,
            'Market', action=lambda: self.city_state('You are in the market.')
            )
        
        temple_btn = Button(
            100, 300, 150, 50, 
            'Temple', action=lambda: self.city_state('The sacred temple.')
            )
        
        blacksmith_btn = Button(
            100, 400, 150, 50, 
            'Blacksmith', action=lambda: self.city_state('You enter the blacksmith store')
            )
        
        return_btn = Button(
            500, 500, 150, 50, 'Return',
            action=lambda: self.change_screen('start_game')
        )
        
        self.widgets.extend([tavern_btn, market_btn,  temple_btn, blacksmith_btn, return_btn])
    
    def init_places(self):
        self.place_widgets = {
            'tavern': [
                Text(300, 50, 100, 'Welcome to the tavern.'),
                Button()
            ],
            'market': [
                
            ],
            'temple':[
                
            ],
            'blacksmith':[
                
            ]
        }
        
    def city_state(self, place_text):
        text_city = Text(
            300, 50, 300, 100,
            text=place_text
        )
        
        self.widgets.append(text_city)