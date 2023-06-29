from core.Items.Item import DecisiveItem
from core.Message import PostAttackMessage
from core.TargetType import Allies


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

        @self.source.session.event_manager.at(self.source.session.id, turn=self.source.session.turn,
                                              event=PostAttackMessage)
        def shield_block(message: PostAttackMessage):
            if message.target != self.target:
                return
            message.damage = 0
