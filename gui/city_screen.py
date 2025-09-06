from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay
from database import MessageLog

class CityScreen(GuiBase):
    def __init__(self, screen, change_screen_callback, app=None):
        super().__init__(screen, change_screen_callback)
        self.current_place = None
        self.current_city  = None
        self.city_places_df = None
        self.place_widgets = {}
        self.app = app
        self.setup_ui()
        
    def setup_ui(self):
        self.main_buttons = []
        return_btn = Button(
            600, 500, 150, 50, 'Return',
            action=lambda: self.change_screen('start_game')
        )
        self.widgets.append(return_btn)
        self.set_city_data()
    
    def set_city_data(self):
        self.current_city = self.app.game_core.current_city
        self.city_places_df = self.app.game_core.tier_city_df
        self.generate_city_ui()
        
    def generate_city_ui(self):
        for widget in self.main_buttons:
            if widget in self.widgets:
                self.widgets.remove(widget)
        self.main_buttons.clear()
        self.place_widgets.clear()

        
        y_position = 100
        
        for _, place_data in self.city_places_df.iterrows():
            btn = Button(
                100, y_position, 150, 50, 
                place_data['name'],
                action=lambda pd=place_data.to_dict(): self.show_place_details(pd)
            )
            self.main_buttons.append(btn)
            self.widgets.append(btn)
            y_position += 60
            
            self.prepare_place_widgets(place_data)
            
    def prepare_place_widgets(self, place_data):
        place_id = place_data['name']
        
        specific_widgets = []
        self.prepare_specific_place_widgets(specific_widgets, place_data)
        
        back_btn = Button(
            600, 450, 100, 40,'Back to city',
            action=lambda: self.show_place_list()
        )
        specific_widgets.append(back_btn)
        self.place_widgets[place_id] = specific_widgets
        
        for widget in specific_widgets:
            widget.visible = False
            
    def prepare_specific_place_widgets(self, widget_list:list, place_data):
        y_position = 50
        
        title_text = Text(300, y_position, 250, 30, f"Welcome to {place_data['name']}")
        widget_list.append(title_text)
        y_position += 40
        
        if place_data['type'] == 'blacksmith' and 'craft' in place_data:
            self.add_blacksmith_widgets(widget_list, place_data, y_position)
        elif place_data['type'] == 'temple' and 'healing_cost' in place_data:
            self.add_temple_widgets(widget_list, place_data, y_position)
        elif place_data['type'] == 'store':
            self.add_store_widgets(widget_list, place_data, y_position)
        elif place_data['type'] == 'tavern' and 'mission' in place_data:
            self.add_tavern_widgets(widget_list, place_data, y_position)      
            
    def add_blacksmith_widgets(self, widget_list, place_data, start_y):
        y = start_y
        craft_text = Text(100, y, 200, 30, "Available crafts:")
        widget_list.append(craft_text)
        y += 40
        
        for item_name, requirements in place_data['craft'].items():
            req_text = f"{item_name}: "
            req_text += ", ".join([f"{qty} {mat}" for mat, qty in requirements.items()])
            
            item_text = Text(120, y, 300, 25, req_text)
            craft_btn = Button(
                500, y, 100, 25, "Craft",
                action=lambda i=item_name, r=requirements: print(f'{i}, {r}')
            )
            widget_list.extend([item_text, craft_btn])
            y += 30
    
    def add_temple_widgets(self, widget_list, place_data, start_y):
        y = start_y
        heal_text = Text(300, y, 250, 30, 
                        f"Healing cost: {place_data['healing_cost']} gold")
        widget_list.append(heal_text)
        y += 40
        
        heal_btn = Button(
            300, y, 150, 50, "Receive Healing",
            action=lambda: print(place_data['healing_cost'])
        )
        widget_list.append(heal_btn)
    
    def add_store_widgets(self, widget_list, place_data, start_y):
        y = start_y
        
        if 'buy_option' in place_data:
            buy_text = Text(250, y, 200, 30, "Items for sale:")
            widget_list.append(buy_text)
            y += 40
            
            for item, price in place_data['buy_option'].items():
                item_text = Text(250, y, 200, 25, f"{item}: {price} gold")
                buy_btn = Button(
                    520, y, 80, 25, "Buy",
                    action=lambda i=item, p=price: print(f'{i}, {p}')
                )
                widget_list.extend([item_text, buy_btn])
                y += 30
        
        if 'sell_option' in place_data:
            sell_text = Text(250, y, 200, 30, "We buy:")
            widget_list.append(sell_text)
            y += 40
            
            for item, price in place_data['sell_option'].items():
                item_text = Text(250, y, 200, 25, f"{item}: {price} gold each")
                sell_btn = Button(
                    520, y, 80, 25, "Sell",
                    action=lambda i=item, p=price: print(f'{i}, {p}')
                )
                widget_list.extend([item_text, sell_btn])
                y += 30
    
    def add_tavern_widgets(self, widget_list, place_data, start_y):
        y = start_y
        mission_text = Text(300, y, 200, 30, "Available missions:")
        widget_list.append(mission_text)
        y += 40
        
        for mission in place_data['mission']:
            mission_btn = Button(
                300, y, 250, 40, mission,
                action=lambda m=mission: print(m)
            )
            widget_list.append(mission_btn)
            y += 50
     
    def show_place_list(self):
        self.hide_current_place()
        self.current_place = None
        for btn in self.main_buttons:
            btn.visible = True
            
    def show_place_details(self, place_data):
        self.hide_current_place()
        
        for btn in self.main_buttons:
            btn.visible = False
            
        place_id = place_data['name']
        
        for widget in self.place_widgets[place_id]:
            widget.visible = True
            if widget not in self.widgets:
                self.widgets.append(widget)
        
        self.current_place = place_id
        
    def hide_current_place(self):
        if self.current_place:
            if self.current_place in self.place_widgets:
                for widget in self.place_widgets[self.current_place]:
                    widget.visible = False
                    if widget in self.widgets:
                        self.widgets.remove(widget)
                        
    # def setup_ui(self):
    #     tavern_btn = Button(
    #         100, 100, 150, 50, 
    #         'Tavern', action=lambda: self.city_state('tavern')
    #         )
        
    #     market_btn = Button(
    #         100, 200, 150, 50,
    #         'Market', action=lambda: self.city_state('market')
    #         )
        
    #     temple_btn = Button(
    #         100, 300, 150, 50, 
    #         'Temple', action=lambda: self.city_state('temple')
    #         )
        
    #     blacksmith_btn = Button(
    #         100, 400, 150, 50, 
    #         'Blacksmith', action=lambda: self.city_state('blacksmith')
    #         )
        
    #     return_btn = Button(
    #         600, 500, 150, 50, 'Return',
    #         action=lambda: self.change_screen('start_game')
    #     )
        
        
    #     self.widgets.extend([tavern_btn, market_btn,  temple_btn, blacksmith_btn, return_btn])

    #     self.init_places()
        
        
    # def init_places(self):
    #     self.place_widgets = {
    #         'tavern': [
    #             Text(300, 50, 100, 50, 'Welcome to the tavern.'),
    #             Button(300, 200, 150, 50, 'Buy Drink',
    #                    action=lambda: MessageLog.add_message("You're drunk!!"))
    #         ],
    #         'market': [
    #             Text(300, 50, 100, 50,'You are in the market.'),
    #             Button(300, 200, 150, 50, 'Buy potion.',
    #                    action=lambda: MessageLog.add_message("You buy some potions!!"))
    #         ],
    #         'temple':[
    #             Text(300, 50, 100, 50,'The sacred temple.'),
    #             Button(300, 200, 150, 50, 'Pray',
    #                    action=lambda: MessageLog.add_message("The Gods blessed you!"))
    #         ],
    #         'blacksmith':[
    #             Text(300, 50, 100, 50,'You enter the blacksmith store.'),
    #             Button(300, 200, 150, 50, 'Craft Weapon',
    #                    action=lambda: MessageLog.add_message("The weapon its forged!"))
    #         ]
    #     }
    #     for place in self.place_widgets.values():
    #         for widget in place:
    #             widget.visible = False
        
    # def city_state(self, place_text):
    #     if self.current_place:
    #         for widget in self.place_widgets[self.current_place]:
    #             widget.visible = False
    #             if widget in self.widgets:
    #                 self.widgets.remove(widget)
        
    #     self.current_place = place_text
    #     for widget in self.place_widgets[place_text]:
    #         widget.visible = True
    #         if widget not in self.widgets:
    #             self.widgets.append(widget)