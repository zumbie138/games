
class ConjuringSpell():
    def __init__(self):
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
        
        
        
