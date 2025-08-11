from abc import ABC, abstractmethod
import pygame

class WidgetBase(ABC):
    '''Classe basica abstrata para todos os widgets'''
    def __init__(self, x:int, y:int, width:int, height:int):
        self.x = x
        self.y = y
        # self.sys_font = pygame.font.SysFont()
        # self.font = pygame.font.Font()
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
    
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        '''Processa eventos do pygame'''
        pass
    
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        '''Desenha widget na superficie'''
        pass
    
    @abstractmethod
    def update(self) -> None:
        '''Atualiza logica do Widget'''
        pass