from core.Items.Item import DecisiveItem
from core.TargetType import Allies, Enemies


class FlashGrenade(DecisiveItem):
    def __init__(self, source):
        super().__init__(source, name='Световая граната', id='flashgrenade', target_type=Enemies())

    def use(self):
        self.target.energy -= 8
        self.target.session.say(f'😵|{self.source.name} кидает световую гранату в {self.target.name}. (-8 Энергии)')
