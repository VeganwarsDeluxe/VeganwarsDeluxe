import random
from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies, Everyone


class RageSerum(FreeItem):
    id = 'rage-serum'
    name = 'Сыворотка бешенства'

    def __init__(self, source):
        super().__init__(source, target_type=Everyone())

    def use(self):
        self.source.session.say(f"💉|{self.source.name} использует сыворотку бешенства на {self.target.name}!")

        @self.source.session.handlers.now(events='post-action')
        def serum_attack(message):
            if self.target.dead:
                return
            attack = self.target.get_action('attack', default=True)
            attack.target = random.choice(attack.targets) if attack.targets else self.target
            attack()