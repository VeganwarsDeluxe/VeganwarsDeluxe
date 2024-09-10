from VegansDeluxe.core import Entity
from VegansDeluxe.core import Session
from VegansDeluxe.core import StateContext, OwnOnly, Enemies, RangedAttack
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core.Skills.Skill import Skill


class Pyrotechnic(Skill):
    id = 'shield-gen'
    name = 'Генератор щитов'
    description = ('В начале игры вы получаете бомбу, которая наносит 1 урона. '
                   'Можно потратить ход, чтобы улучшить её на +2 урона, число улучшений не ограничено.')

    def __init__(self):
        super().__init__()
        self.damage = 1


# @RegisterState(Pyrotechnic)
# TODO: FIX PYROTECHNIC
async def register(root_context: StateContext[Pyrotechnic]):
    session: Session = root_context.session
    source = root_context.entity


# @AttachedAction(Pyrotechnic)
class LaunchBomb(RangedAttack):
    id = 'launch-bomb'
    name = 'Кинуть бомбу'
    target_type = Enemies().distance.ANY

    def __init__(self, session: Session, source: Entity, skill: Pyrotechnic):
        super().__init__(session, source)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.state.damage == 0

    @property
    def blocked(self):
        return self.source.energy < 2

    def calculate_damage(self, source: Entity, target: Entity) -> int:
        return self.state.damage

    async def func(self, source, target):
        await super().func(source, target)
        self.state.damage += 2
        self.session.say(f"⚒|Пиротехник {source.name} улучшает самодельную бомбу.")


# @AttachedAction(Pyrotechnic)
class ImproveBomb(DecisiveStateAction):
    id = 'improve-bomb'
    name = 'Улучшить бомбу'
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: Pyrotechnic):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return self.state.damage == 0

    async def func(self, source, target):
        self.state.damage += 2
        self.session.say(f"⚒|Пиротехник {source.name} улучшает самодельную бомбу.")
