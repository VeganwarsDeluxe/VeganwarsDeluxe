from core.Items.Item import DecisiveItem
from core.TargetType import Enemies


class FlashGrenade(DecisiveItem):
    id = 'flashgrenade'
    name = 'Световая граната'

    def __init__(self, source):
        super().__init__(source, target_type=Enemies())

    def use(self):
        self.target.energy -= 8
        self.target.session.say(f'😵|{self.source.name} кидает световую гранату в {self.target.name}. (-8 Энергии)')
