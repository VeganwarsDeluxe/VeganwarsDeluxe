from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies, Everyone


class Shield(DecisiveItem):
    id = 'shield'
    name = 'Щит'

    def __init__(self, source):
        super().__init__(source, target_type=Allies())

    def use(self):
        if self.target == self.source:
            self.target.session.say(f"🔵|{self.source.name} использует щит. Урон отражен!")
        else:
            self.target.session.say(f"🔵|{self.source.name} использует щит на {self.target.name}. Урон отражен!")

        @self.source.session.event_manager.at(turn=self.source.session.turn, events='post-attack')
        def shield_block():
            attack = self.source.session.event.action
            if not attack.target:
                return
            if attack.target != self.target:
                return
            damage = attack.data.get('damage')
            if not damage:
                return
            attack.data.update({'damage': 0})
