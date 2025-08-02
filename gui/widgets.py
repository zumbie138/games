import pygame

class Button():
    def __init__(self, x, y, width, height, text, action = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.normal_color = (255, 0, 0)
        self.hover_color = (255, 255, 0)
        self.current_color = self.normal_color
        self.font = pygame.font.Font('Aerial', 24)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.current_color = self.hover_color if self.rect.collidepoint(event.pos) else self.normal_color