from core.Skills.Skill import Skill
from modern.Items.RageSerum import RageSerum


class Alchemist(Skill):
    id = 'alchemist'
    name = 'Алхимик'
    description = 'В начале игры и каждые 9 ходов дает вам сыворотку бешенства, применение ' \
                  'которой заставляет выбранную цель атаковать дополнительно к своему действию..'

    def __init__(self, source):
        super().__init__(source, stage='pre-move')

    def __call__(self):
        if self.source.session.turn == 1:
            @self.source.session.handlers.every(turns=9, events='pre-move')
            def give_serum(message):
                self.source.items.append(RageSerum(self.source))
