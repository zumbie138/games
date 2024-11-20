from database import GameBase
from core import GameCore

class ConjuringSpell(GameBase):
    def __init__(self):
        self.df_spells = self.get_database_dataframe('spells_database.json')
        self.game_core = GameCore()
        self.spells_cooldown = {}
        self.spells_duration = {}
        
    def add_spell_timers(self, name:str, cooldown:int, duration:int):
        self.spells_cooldown[name] = cooldown
        self.spells_duration[name] = duration
    
    def _decrement_and_clean(self,spell_timer:dict):
        for spell in list(spell_timer.keys()):
            spell_timer[spell] -= 1
    
    def check_duration_spell(self):
        for spell in list(self.spells_duration.keys()):
            if self.spells_duration[spell] <= 0:
                del self.spells_duration[spell]
                return spell
    
    def update_spell_timer(self):
        self._decrement_and_clean(self.spells_cooldown)
        self._decrement_and_clean(self.spells_duration)
        
    def calculate_conjured_spell(self,damage_base:int, healing_base:int, vitality:float, intelligence:float, charisma:float):
        spell_damage = damage_base * (1 + (((intelligence  +(charisma/2)) * 3) / 10)) 
        healing_done = healing_base * (1 + (((intelligence + (vitality/2) + (charisma/5)) * 3) / 10))
        return spell_damage, healing_done
        
    def check_active_durations(self):
        self.update_spell_timer()
        effect_over = self.check_duration_spell()
        if effect_over is not None:
            buff_removed = self.get_info_by_name(effect_over,'name','buff',self.df_spells)
            print(buff_removed)
            print(self.buffs)
            self.game_core.remove_buff(buff_removed)
            self.game_core.update_character()
        
    def conjuring_core(self,spell_list:list,inteligence:float,charisma:float):
        for spell in reversed(spell_list):
            spell_info = self.filter_dataframe_by_name(spell,'name',self.df_spells)
            rate = spell_info['rate'].item()
            mana_spell = spell_info['mana'].item()
            if spell in self.spells_cooldown:
                cooldown = self.spells_cooldown[spell]
            else:
                cooldown = 0
            if cooldown <= 0:
                if self.player.mana >= mana_spell:
                    final_rate = rate + charisma*1.3 + inteligence*0.3
                    roll_dice = self.get_random_in_interval((0, 100))
                    if roll_dice <= final_rate:
                        print(f'You conjure {spell} !')
                        self.conjure_spell(spell, spell_info)
                        break
                
    def conjure_spell(self, spell_name:str, spell_info):
        mana_spell = spell_info['mana'].item()
        damage_base = spell_info['damage'].item()
        heal_base = spell_info['heal'].item()
        spell_cooldown = spell_info['cooldown'].item()
        spell_duration = spell_info['duration'].item()
        buff_tuple = spell_info['buff'].item()
        self.conjuring_spell.add_spell_timers(spell_name, spell_cooldown, spell_duration)
        self.player.mana = self.player.mana - mana_spell
        if spell_info['type'].item() == 'passive' or spell_info['type'].item() == 'buff':
            self._add_buff(buff_tuple)
            print(buff_tuple)
            print(self.buffs)
            self._update_character()
        elif spell_info['type'].item() == 'offensive' or spell_info['type'].item() == 'healing':
            spell_result = self.conjuring_spell.calculate_conjured_spell(damage_base,heal_base,self.player.vitality,self.player.intelligence,self.player.charisma)           
            self.apply_magic_damage(*spell_result)
            
    def apply_magic_damage(self,magic_damage:float, healing_done:float):
        self.monster.life = self.monster.life - magic_damage
        self.player.life = self.player.life + healing_done
        if self.player.life > self.player.max_life:
            self.player.life = self.player.max_life
        if magic_damage > 0:
            print(f'Your magic deals {magic_damage:.2f} hit points.')
        if healing_done > 0:
            print(f'You heal yourself {healing_done:.2f} hit points.')
