from core.Skills.Skill import Skill
from modern.Items.Stimulator import Stimulator


class Medic(Skill):
    def __init__(self, source):
        super().__init__(source, id='medic', name='Медик', stage='pre-move')
        self.description = 'В начале боя вы получаете стимулятор, восстанавливающий 2 хп при использовании.'

    def __call__(self):
        if self.source.session.turn == 1:
            self.source.items.append(Stimulator(self.source))
