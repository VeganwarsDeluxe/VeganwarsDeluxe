from core.Items.Item import DecisiveItem, FreeItem
from core.TargetType import Allies, Everyone


class Hitin(FreeItem):
    id = 'hitin'
    name = 'Хитин'

    def __init__(self, source):
        super().__init__(source, target_type=Everyone())

    def use(self):
        self.target.get_skill('armor').add(2, 100)
        self.target.session.say(f'💉|{self.source.name} использует хитин на {self.target.name}!')

        @self.source.session.handlers.at(turn=self.source.session.turn + 2, events='post-damages')
        def hitin_knockout():
            self.target.get_skill('armor').remove((2, 100))
            self.target.get_skill('stun').stun += 1
            self.source.session.say(f'🌀|{self.target.name} теряет эффект хитина. Игрок оглушен!')
