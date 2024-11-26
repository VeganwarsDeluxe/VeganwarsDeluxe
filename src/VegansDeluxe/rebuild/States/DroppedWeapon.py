from VegansDeluxe.core import AttachedAction, OwnOnly
from VegansDeluxe.core import Entity
from VegansDeluxe.core import Session
from VegansDeluxe.core import State
from VegansDeluxe.core.Actions.StateAction import DecisiveStateAction
from VegansDeluxe.core.Translator.LocalizedString import ls
from VegansDeluxe.rebuild.Weapons.Fist import Fist


class DroppedWeapon(State):
    id = 'dropped-weapon'

    def __init__(self):
        super().__init__()
        self.weapon = None
        self.default_weapon_type = Fist

    def drop_weapon(self, source: Entity):
        self.weapon = source.weapon
        source.weapon = self.default_weapon_type(source.session_id, source.id)

    def pick_up_weapon(self, source: Entity):
        source.weapon = self.weapon
        self.weapon = None


@AttachedAction(DroppedWeapon)
class PickUp(DecisiveStateAction):
    id = 'pick_up'
    name = ls("rebuild.state.dropped_weapon.name")
    target_type = OwnOnly()

    def __init__(self, session: Session, source: Entity, skill: DroppedWeapon):
        super().__init__(session, source, skill)
        self.state = skill

    @property
    def hidden(self) -> bool:
        return not self.state.weapon

    async def func(self, source, target):
        source.weapon = self.state.weapon
        self.session.say(ls("rebuild.state.dropped_weapon.text").format(source.name))
        self.state.weapon = None
