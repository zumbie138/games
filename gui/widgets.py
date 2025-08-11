import pygame
from gui.widget_base import WidgetBase

'''classe destinada a botoes em geral'''
class Button(WidgetBase):
    def __init__(self, x, y, width, height, text, action = None, enable=True):
        super().__init__(x,y,width, height)
        self.text = text
        self.action = action
        self.enable = enable
        
        self.normal_color = (255, 0, 0)
        self.hover_color = (255, 255, 0)
        self.disable_color = (50, 50, 50)
        self.current_color = self.normal_color
        self.font = pygame.font.Font(None, 24)
        
    def handle_event(self, event:pygame.event.Event) -> None:
        if not self.enable or not self.visible:
            return
        
        if event.type == pygame.MOUSEMOTION:
            self.current_color = self.hover_color if self.rect.collidepoint(event.pos) else self.normal_color
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
                
    def draw(self, surface:pygame.Surface) -> None:
        if not self.visible:
            return
        
        color = self.disable_color if not self.enable else self.current_color
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)
        
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
    
    def update(self) -> None:
        #implementar alguma mudança de estado aqui
        pass
    
    
'''classe destinada a campos de texto input'''
class TextInput(WidgetBase):
    def __init__(self, x, y, width, height, placeholder='', max_length=20, on_change=None):
        super().__init__(x, y, width, height)
        
        #atributos especificos
        self.placeholder = placeholder
        self.text = ''
        self.active = False
        self.max_length = max_length
        self.font = pygame.font.Font(None, 24)
        self.on_change = on_change
        
        #cores
        self.color = (255, 255, 255)
        self.bg_color = (50, 50, 50)
        self.placeholder_color = (150, 150, 150)
        
    def handle_event(self, event:pygame.event.Event) -> bool:
        if not self.visible:
            return False
        
        text_changed = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            return self.active
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                text_changed = True
            elif len(self.text) < self.max_length:
                self.text += event.unicode
                text_changed = True
                
            if text_changed and self.on_change:
                self.on_change(self.text)
                
            return text_changed
        
        return False
    
    def draw(self, surface:pygame.Surface) -> None:
        if not self.visible:
            return 
        
        pygame.draw.rect(surface, self.bg_color, self.rect)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2)
        
        if not self.text and not self.active:
            text_surf = self.font.render(self.placeholder, True, self.placeholder_color)
        else:
            text_surf = self.font.render(self.text, True, self.color)
        
        text_rect = text_surf.get_rect(
            midleft=(self.rect.x +5, self.rect.centery)
        )
        surface.blit(text_surf, text_rect)
        
        if self.active:
            if pygame.time.get_ticks() % 1000 < 500:
                cursor_pos = self.font.size(self.text)[0] + self.rect.x + 5
                pygame.draw.line(
                    surface, self.color,
                    (cursor_pos, self.rect.y + 5),
                    (cursor_pos, self.rect.y + self.rect.height - 5),
                    2
                )
    
    def update(self):
        pass
    
    
'''classe destinada a imprimir textos nas telas'''
class Text(WidgetBase):
    def __init__(self, x, y, width, height, text, font_size=24, color=(255,255,255), font_name=None):
        super().__init__(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        
    def draw(self, surface:pygame.Surface):
        if self.visible:
            text_surface = self.font.render(self.text, True, self.color)
            surface.blit(text_surface, (self.rect.x, self.rect.y))
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
            
'''classe destidana a imprimir o personagem nas telas'''
class PlayerStatusDisplay(WidgetBase):
    def __init__(self, x, y, width, height, game_core=None):
        super().__init__(x, y, width, height)
        self.game_core = game_core
        self.title_font = pygame.font.SysFont(None, 24)
        self.font = pygame.font.SysFont(None, 20, bold=True)
        self.color = (255,255,255)
        self.bg_color = (50,50,50,150)
        self.padding = 10
        
    def draw(self, surface:pygame.Surface):
        if not hasattr(self.game_core, 'player') or not self.game_core.player:
            return
        
        player = self.game_core.player
        
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, self.bg_color, bg_surface.get_rect(), border_radius=5)
        surface.blit(bg_surface, self.rect)
        
        y_offset = self.padding
        x_pos = self.rect.x + self.padding
        
        title = self.title_font.render(f'{player.name} - Lvl :{player.level}', True, (255, 215, 0))
        surface.blit(title, (x_pos, self.rect.y + y_offset))
        
        y_offset += title.get_height() + 15
        
        attributes = [
            f"Raça: {player.race} | Classe: {player.class_type}",
            f"HP: {player.life:.2f}/{player.max_life}",
            f"Mana: {player.mana:.2f}/{player.max_mana}",
            f"EXP: {player.experience}",
            f"Força: {player.strength:.2f} | Agilidade: {player.agility:.2f}",
            f"Vitalidade: {player.vitality:.2f} | Inteligência: {player.intelligence:.2f}",
            f"Ataque: {player.attack:.2f} | Defesa: {player.defense:.2f}"
        ]
        
        for attr in attributes:
            text = self.font.render(attr, True, self.color)
            surface.blit(text, (x_pos, self.rect.y + y_offset))
            y_offset += text.get_height() + 5
            
    def update(self):
        pass
    
    def handle_event(self, event):
        pass