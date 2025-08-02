import pygame

class GuiBase():
    def __init__(self, screen, chage_screen_callback):
        self.screen = screen
        self.change_screen = chage_screen_callback
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.widgets = []
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False