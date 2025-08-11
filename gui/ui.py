import pygame
from gui.widget_base import WidgetBase

class GuiBase():
    def __init__(self, screen, change_screen_callback, app=None):
        self.screen = screen
        self.change_screen = change_screen_callback
        self.widgets: list[WidgetBase] = []
    
    def handle_events(self, event):
            for widget in self.widgets:
                widget.handle_event(event)
    
    def update(self):
        for widget in self.widgets:
            widget.update()
            
    def draw(self):
        self.screen.fill((0, 0, 0))
        for widget in self.widgets:
            widget.draw(self.screen)