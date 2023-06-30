from core.Items.ItemAction import FreeItem
from core.Events.Events import PostDamagesGameEvent
from core.TargetType import Everyone


class Hitin(FreeItem):
    id = 'hitin'
    name = 'Хитин'

    def __init__(self, source):
        super().__init__(source, target_type=Everyone())

    def use(self, source, target):
        target.get_skill('armor').add(2, 100)
        target.session.say(f'💉|{self.source.name} использует хитин на {target.name}!')

        # TODO: self.source.session.turn
        @self.source.session.event_manager.at(self.source.session.id, turn=self.source.session.turn + 2,
                                              event=PostDamagesGameEvent)
        def hitin_knockout(message: PostDamagesGameEvent):
            target.get_skill('armor').remove((2, 100))
            target.get_skill('stun').stun += 1
            source.session.say(f'🌀|{self.target.name} теряет эффект хитина. Игрок оглушен!')
