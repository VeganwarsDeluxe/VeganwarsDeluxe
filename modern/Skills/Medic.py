from core.Skills.Skill import Skill
from modern.Items.Stimulator import Stimulator


class Medic(Skill):
    id = 'medic'
    name = 'Медик'
    description = 'В начале боя вы получаете стимулятор, восстанавливающий 2 хп при использовании.'

    def register(self, session_id):
        self.source.items.append(Stimulator(self.source))
