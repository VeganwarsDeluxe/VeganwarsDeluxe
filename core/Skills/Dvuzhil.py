from .Skill import Skill
from core.Entities.Entity import Entity
import random


class Dvuzhil(Skill):
    def __init__(self):
        super().__init__(id='dvuzhil', name='Двужильность', stage='pre-move')

    def __call__(self, source: Entity):
        if source.session.turn == 0:
            source.hp += 1
            source.say('Я получил 1 хп от двужильности.')
