from core.Items.Item import FreeItem
from core.Events import PostDamagesEvent
from core.TargetType import Everyone


class Hitin(FreeItem):
    id = 'hitin'
    name = 'Хитин'

    def __init__(self, source):
        super().__init__(source, target_type=Everyone())

    def use(self):
        self.target.get_skill('armor').add(2, 100)
        self.target.session.say(f'💉|{self.source.name} использует хитин на {self.target.name}!')

        # TODO: self.source.session.turn
        @self.source.session.event_manager.at(self.source.session.id, turn=self.source.session.turn + 2,
                                              event=PostDamagesEvent)
        def hitin_knockout(message: PostDamagesEvent):
            self.target.get_skill('armor').remove((2, 100))
            self.target.get_skill('stun').stun += 1
            self.source.session.say(f'🌀|{self.target.name} теряет эффект хитина. Игрок оглушен!')
