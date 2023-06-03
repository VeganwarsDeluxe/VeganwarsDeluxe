from .Skill import Skill
from core.Entities.Entity import Entity
import random


class Armor(Skill):
    def __init__(self):
        super().__init__(id='armor', name='Броня', stage='attack')

    def __call__(self, source: Entity):
        if random.randint(0, 100) > 15:
            return
        damage = 0
        entity = source
        for entity in source.session.entities:
            if entity.action.data.get('target') == source:
                damage = entity.action.data.get('damage')
                break
            return
        if entity.action.data.get('armored'):
            return
        entity.action.data.update({'armored': True})
        if damage == 0:
            return
        source.say(f'Броня отработала! Урон уменьшен c {damage} до {damage - 1}!')
        entity.action.data.update({'damage': damage - 1})
