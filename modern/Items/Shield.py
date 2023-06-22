from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies, Everyone


class Shield(DecisiveItem):
    def __init__(self, source):
        super().__init__(source, name='Щит', id='shield', target_type=Allies())

    def use(self):
        if self.target == self.source:
            self.target.session.say(f"🔵|{self.source.name} использует щит. Урон отражен!")
        else:
            self.target.session.say(f"🔵|{self.source.name} использует щит на {self.target.name}. Урон отражен!")

        @self.source.session.handlers.at(turn=self.source.session.turn, events='post-attack')
        def shield_block():
            for entity in self.source.session.entities:
                if entity.action.id != 'attack':
                    continue
                attack_target = entity.action.data.get('target')
                if not attack_target:
                    continue
                if attack_target != self.source:
                    continue
                damage = entity.action.data.get('damage')
                if not damage:
                    continue
                entity.action.data.update({'damage': 0})
