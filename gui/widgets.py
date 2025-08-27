import pygame
from gui.widget_base import WidgetBase
from typing import List, Tuple
from database.game_repository import MessageLog

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
            f'Charisma: {player.charisma:.2f}',
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
    
'''classe destinada a imprimir monstros na tela'''
class MonsterStatusDisplay(WidgetBase):
    def __init__(self, x, y, width, height, game_core=None):
        super().__init__(x, y, width, height)
        self.game_core = game_core
        self.title_font = pygame.font.SysFont(None, 24)
        self.font = pygame.font.SysFont(None, 20, bold=True)
        self.color = (255,255,255)
        self.bg_color = (50,50,50,150)
        self.padding = 10
        
    def draw(self, surface:pygame.Surface):
        if not hasattr(self.game_core, 'monster') or not self.game_core.monster:
            return
        
        monster = self.game_core.monster
        
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, self.bg_color, bg_surface.get_rect(), border_radius=5)
        surface.blit(bg_surface, self.rect)
        
        y_offset = self.padding
        x_pos = self.rect.x + self.padding
        
        title = self.title_font.render(f'{monster.name} - Lvl :{monster.level}', True, (255, 215, 0))
        surface.blit(title, (x_pos, self.rect.y + y_offset))
        
        y_offset += title.get_height() + 15
        
        attributes = [
            f"Type: {monster.type} | Level: {monster.level}",
            f"HP: {monster.life:.2f}/{monster.max_life}",
            f"Ataque: {monster.attack:.2f} | Defesa: {monster.defense:.2f}"
        ]
        
        for attr in attributes:
            text = self.font.render(attr, True, self.color)
            surface.blit(text, (x_pos, self.rect.y + y_offset))
            y_offset += text.get_height() + 5
            
    def update(self):
        pass
    
    def handle_event(self, event):
        pass
    
'''Classe destinada a fazer um Journal de logs de mensagem de açoes no jogo'''
class Journal(WidgetBase):
    def __init__(self, x, y, width, height, max_lines=100, toggle_callback = None):
        super().__init__(x, y, width, height)
        self.messages: List[Tuple[str, tuple[int, int, int]]] = []
        self.max_lines = max_lines
        self.font = pygame.font.SysFont(None, 18)
        self.scroll_offset = 0
        self.line_height = 22
        self.visible = False
        self.background_color = (40, 40, 50, 220)
        self.scroll_bar_color = (100, 100, 120)
        self.scroll_bar_width = 10
        self.toggle_callback = toggle_callback
        
    def add_entry(self, text: str, color=(255, 255, 255)):
        self.messages.append((text, color))
        if len(self.messages) > self.max_lines:
            self.messages.pop(0)
    
    def handle_event(self, event):
        if not self.visible:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                self.scroll_offset = max(0, self.scroll_offset-1)
                return True
            elif event.button == 5:
                max_offset = max(0, len(self.messages) - self.rect.height // self.line_height)
                self.scroll_offset = min(max_offset, self.scroll_offset +1)
                return True
                
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 1)
                return True
            elif event.key == pygame.K_DOWN:
                max_offset = max(0, len(self.messages) - self.rect.height // self.line_height)
                self.scroll_offset = min(max_offset, self.scroll_offset +1)
                return True
        return False
        
    def draw(self, surface):
        if not self.visible:
            return
        
        bg_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, self.background_color, bg_surface.get_rect(), border_radius=5)
        surface.blit(bg_surface, self.rect)
        
        text_area = pygame.Rect(
            self.rect.x + 5,
            self.rect.y + 5,
            self.rect.width -15,
            self.rect.height - 10
        )
        
        old_clip = surface.get_clip()
        surface.set_clip(text_area)
        
        visivible_lines = self.rect.height // self.line_height
        start_idx = max(0, len(self.messages) - visivible_lines - self.scroll_offset)
        
        y_pos = self.rect.y + 5
        for i in range(start_idx, len(self.messages)):
            if y_pos > self.rect.y + self.rect.height:
                break
            
            text, color = self.messages[i]
            text_surface = self.font.render(text, True, color)
            surface.blit(text_surface, (self.rect.x + 5, y_pos))
            y_pos += self.line_height
        
        surface.set_clip(old_clip)
        
        self._draw_scrollbar(surface)
        
    def _draw_scrollbar(self, surface):
        if len(self.messages) <= self.rect.height // self.line_height:
            return
        
        total_lines = len(self.messages)
        visible_lines = self.rect.height // self.line_height
        scrollbar_height = max(20, (visible_lines / total_lines) * self.rect.height)
        
        scroll_ratio = self.scroll_offset / (total_lines - visible_lines)
        scroll_y = self.rect.y + scroll_ratio * (self.rect.height - scrollbar_height)
        
        scroll_rect = pygame.Rect(
            self.rect.right - self.scroll_bar_width - 2,
            scroll_y,
            self.scroll_bar_width,
            scrollbar_height
        )
        
        pygame.draw.rect(surface, self.scroll_bar_color, scroll_rect, border_radius=5)
        
    def toggle_visibility(self):
        self.visible = not self.visible
        if self.toggle_callback:
            self.toggle_callback(self.visible)
        
    def update(self):
        pass

'''classe destinada a fazer o inventario'''
class InventoryWidget(WidgetBase):
    def __init__(self, x, y, width, height, game_core):
        super().__init__(x, y, width, height)
        self.game_core = game_core
        self.dragging_item = None
        self.drag_offset = (0, 0)
        self.slot_rects = {}
        self.item_rects = {}
        self.font = pygame.font.Font(None, 20)
        self.title_font = pygame.font.Font(None, 24)
        self.slot_size = (60, 60)
        self.item_size = (50, 50)
        self.spacing = 10
        
        self.slot_positions = {
            'head': (x + 20, y + 50),
            'neck': (x + 20, y + 120),
            'torso': (x + 20, y + 190),
            'arms': (x + 20, y + 260),
            'right hand': (x + 20, y + 330),
            'left hand': (x + 20, y + 400),
            'waist': (x + 20, y + 470),
            'legs': (x + 90, y + 50),
            'foot': (x + 90, y + 120),
            'finger': (x + 90, y + 190),
            'wrist': (x + 90, y + 260),
            'ears': (x + 90, y + 330),
            'back': (x + 90, y + 400)
        }
        self.inventory_area = pygame.Rect(x + 200, y + 50, width - 220, height - 70)
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=3)
        
        font = pygame.font.SysFont(None, 18)
        text = font.render(self.item_name, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.rect.center)
        surface.blit(text, text_rect)
    
    def handle_event(self, event):
        if not self.visible:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.handle_mouse_down(event)
            
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.handle_mouse_up(event)
                
    def handle_mouse_down(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        for item_name, rect in self.item_rects.items():
            if rect.collidepoint(mouse_pos):
                self.dragging_item = item_name
                self.drag_offset = (mouse_pos[0] - rect.x, mouse_pos[1] - rect.y)
                break
    
    def handle_mouse_up(self, event):
        if not self.dragging_item:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        
        for slot_name, slot_rect in self.slot_rects.items():
            if slot_rect.collidepoint(mouse_pos):
                success = self.game_core.itens_core.equip_item(self.dragging_item, slot_name)
                if success:
                    MessageLog.add_message(f'Equiped {self.dragging_item} in {slot_name}')
                else:
                    MessageLog.add_message(f'Cannot equip {self.dragging_item} in {slot_name}')
                break
            
        self.dragging_item = None
        
    def update(self):
        self.update_item_rects()
        self.update_slot_rects() 
    
    def update_item_rects(self):
        self.item_rects.clear()
        
        x, y =self.inventory_area.x + 10, self.inventory_area.y +10
        col, row = 0, 0
        
        equippable_item = self.game_core.itens_core.get_equippable_items()
        
        for item in equippable_item:
            item_rect = pygame.Rect(x, y, self.item_size[0], self.item_size[1])
            self.item_rects[item['name']] = item_rect
            
            x += self.item_size[0] + self.spacing
            col += 1
            
            if col >= 4:
                col = 0
                x = self.inventory_area.x + 10
                y += self.item_size[1] + self.spacing
                row += 1
                
    def update_slot_rects(self):
        self.slot_rects.clear()
        for slot_name, pos in self.slot_positions.items():
            slot_rect = pygame.Rect(pos[0], pos[1], self.slot_size[0], self.slot_size[1])
            self.slot_rects[slot_name] = slot_rect
    
    def draw(self, surface:pygame.Surface):
        if self.visible:
            return
        
        pygame.draw.rect(surface, (40,40,40), self.rect)
        pygame.draw.rect(surface, (80,80,80), self.rect, 2)
        
        title = self.title_font.render('Equipament & Inventory', True, (255,255,255))
        surface.blit(title, (self.x + 10, self.y+10))
        
        self.draw_equipment_slot(surface)

        pygame.draw.rect(surface, (30,30,30), self.inventory_area)
        pygame.draw.rect(surface, (100,100,100), self.inventory_area, 2)
        
        self.draw_inventory_itens(surface)
        
        if self.dragging_item:
            self.draw_dragging_item(surface)
            
    def draw_equipment_slot(self, surface:pygame.Surface):
        for slot_name, rect in self.slot_rects.items():
            pygame.draw.rect(surface, (40,40,40), rect)
            pygame.draw.rect(surface, (80,80,80), rect, 2)
            
            slot_text = self.font.render(slot_name[:4], True, (255,255,255))
            surface.blit(slot_text, (rect.x +5, rect.y + 5))
            
            equipped_item = self.game_core.player.wearing[slot_name]
            if equipped_item:
                item_color = (150, 200, 150)
                pygame.draw.rect(surface, item_color,
                                 pygame.Rect(rect.x +5, rect.y +5, 
                                             self.item_size[0], self.item_size[1]))
                
                item_text = self.font.render(equipped_item[:3], True, (0,0,0))
                surface.blit(item_text, (rect.x + 15, rect.y + 20))
            
    def draw_inventory_itens(self, surface:pygame.Surface):
        equippable_items = self.game_core.itens_core.get_equippable_items()
        
        for item_name, rect in self.item_rects.items():
            item_info = next((item for item in equippable_items if item['name'] == item_name), None)
            if item_info:
                slot_colors = {
                    'head': (200, 150, 150),
                    'torso': (150, 200, 150),
                    'arms': (150, 150, 200),
                    'legs': (200, 200, 150),
                    'foot': (200, 150, 200),
                    'default': (180, 180, 180)
                }
                
                color = slot_colors.get(item_info['slot_type'], slot_colors['default'])
                pygame.draw.rect(surface, color, rect)
                pygame.draw.rect(surface, (100, 100, 100), rect, 1)
                
                name_text = self.font.render(item_name[:4], True, (0, 0, 0))
                quant_text = self.font.render(str(item_info['quantity']), True, (255, 255, 255))
                
                surface.blit(name_text, (rect.x + 5, rect.y + 5))
                surface.blit(quant_text, (rect.x + 35, rect.y + 35))
                
    def draw_dragging_item(self, surface:pygame.Surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        item_rect = pygame.Rect(mouse_x - self.drag_offset[0], 
                              mouse_y - self.drag_offset[1],
                              self.item_size[0], self.item_size[1])
        
        pygame.draw.rect(surface, (255, 200, 100), item_rect)
        pygame.draw.rect(surface, (200, 150, 50), item_rect, 2)
        
        name_text = self.font.render(self.dragging_item[:4], True, (0, 0, 0))
        surface.blit(name_text, (item_rect.x + 5, item_rect.y + 5))