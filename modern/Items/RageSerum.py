import random
from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies, Everyone


class RageSerum(FreeItem):
    def __init__(self, source):
        super().__init__(source, name='Сыворотка бешенства', id='rage-serum', target_type=Everyone())

    def use(self):
        attack = self.target.get_action('attack', default=True)
        attack.target = random.choice(attack.targets) if attack.targets else self.target
        self.target.session.say(f"💉|{self.source.name} использует сыворотку бешенства на {self.target.name}!")

        @self.source.session.handlers.at(turn=self.source.session.turn, events='post-action')
        def serum_attack():
            attack()
