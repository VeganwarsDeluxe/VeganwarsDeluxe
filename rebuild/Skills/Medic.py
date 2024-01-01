from core.ContentManager import RegisterState
from core.Context import StateContext
from core.Sessions import Session
from core.Skills.Skill import Skill
from rebuild.Items.Stimulator import Stimulator


class Medic(Skill):
    id = 'medic'
    name = 'Медик'
    description = 'В начале боя вы получаете стимулятор, восстанавливающий 2 хп при использовании.'


@RegisterState(Medic)
def register(root_context: StateContext[Medic]):
    session: Session = root_context.session
    source = root_context.entity

    source.items.append(Stimulator())
