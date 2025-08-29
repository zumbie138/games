from gui.ui import GuiBase
from gui.widgets import Button, Text, PlayerStatusDisplay, InventoryWidget

class RefugeScreen(GuiBase):
    def __init__(self, screen, change_screen_callback, app=None):
        super().__init__(screen, change_screen_callback)
        self.current_object = None
        self.app = app
        self.inventory_widget = None
        self.setup_ui()
        
    def setup_ui(self):
        
        refuge_text = Text(
                100, 50, 100, 50,
                'Welcome to your house, what you want to do'
                )
        player_display = PlayerStatusDisplay(
                500, 100, 280, 200,
                game_core=self.app.game_core
            )
        bed_btn = Button(
                100, 100, 150, 50, 'Sleep in bed',
                action=lambda: self.refuge_state('bed')
            )
        train_btn = Button(
                100, 200, 150, 50, 'Train',
                action=lambda: self.refuge_state('training_choice')
            )
        wardobe_btn = Button(
                100, 300, 150, 50, 'Wardobe',
                action=lambda: self.refuge_state('wardobe')
            )
        # mirror_btn = Button(
        #         100, 400, 150, 50, 'Mirror',
        #         action=lambda: self.app.game_core.show_character_core()
        #     )
        return_btn = Button(
                600, 500, 150, 50, 'Return',
                action=lambda: self.change_screen('start_game')
            )
        
        self.widgets.extend([refuge_text, player_display, bed_btn, train_btn, wardobe_btn, return_btn])
        self.init_objects()
        
        
    def init_objects(self):
        self.inventory_widget = InventoryWidget(
            100, 100, 600, 400, self.app.game_core
        )
        self.inventory_widget.visible = False
        
        self.object_widgets = {
            'bed':[
                Text(300, 150, 100, 50, "You're sleeping now."),
                Button(300, 200, 150, 50, 'Stop sleeping',
                       action=lambda: self.stop_action('bed'))
            ],
            'training_choice':[
                Button(
                260, 100, 100, 40, 'Strenght.',
                action=lambda: self.refuge_state('training', 'strength')
                ),
                Button(
                260, 150, 100, 40, 'Agility.',
                action=lambda: self.refuge_state('training', 'agility')
                ),
                Button(
                260, 200, 100, 40, 'Vitality.',
                action=lambda: self.refuge_state('training', 'vitality')
                ),
                Button(
                260, 250, 100, 40, 'Intelligence.',
                action=lambda: self.refuge_state('training', 'intelligence')
                ),
                Button(
                260, 300, 100, 40, 'Charisma.',
                action=lambda: self.refuge_state('training', 'charisma')
                ),
                Button(
                260, 350, 90, 30, 'go back.',
                action=lambda: self.stop_action('train')
                ),
            ],
            'training':[
                Text(300, 50, 100, 50, "You're training now."),
                Button(300, 200, 150, 50, 'Stop training',
                       action=lambda: self.stop_action('train'))
            ],
            'wardobe':[
                Text(300, 50, 100, 50, "This is your wardobe"),
                Button(500, 500, 150, 50, 'Close wardobe',
                       action=lambda: self.stop_action('wardobe'))
            ]
        }
        
        for object in self.object_widgets.values():
            for widget in object:
                widget.visible = False

        self.widgets.append(self.inventory_widget)
        
    def refuge_state(self, object_text, train_type = None):
        if self.current_object:
            for widget in self.object_widgets[self.current_object]:
                widget.visible = False
                if widget in self.widgets:
                    self.widgets.remove(widget)
                    
        self.current_object = object_text
        
        if object_text == 'wardobe':
            self.inventory_widget.visible = True
        else:
            self.inventory_widget.visible = False
            
        if object_text == 'training':
            self.app.run_train_status(train_type)
        elif object_text == 'bed':
            self.app.run_sleep_status()
            
        for widget in self.object_widgets[object_text]:
            widget.visible = True 
            if widget not in self.widgets:
                self.widgets.append(widget)
    
    def stop_action(self, type):
        match type:
            case 'bed':
                self.app.game_core.stop_sleeping()
            case 'train':
                self.app.game_core.stop_training()
            case 'wardobe':
                self.inventory_widget.visible = False
        
        if self.current_object:
            for widget in self.object_widgets[self.current_object]:
                widget.visible = False
                if widget in self.widgets:
                    self.widgets.remove(widget)
            self.current_object = None