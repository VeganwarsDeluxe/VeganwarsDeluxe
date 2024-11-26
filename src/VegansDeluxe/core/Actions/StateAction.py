from VegansDeluxe.core.Actions.Action import Action, FreeAction, DecisiveAction, InstantAction
from VegansDeluxe.core.Entities import Entity
from VegansDeluxe.core.Session import Session
from VegansDeluxe.core.States import State


class StateAction(Action):
    def __init__(self, session: Session, source: Entity, state: State):
        super().__init__(session, source)
        self.state = state


class FreeStateAction(StateAction, FreeAction):
    pass


class DecisiveStateAction(StateAction, DecisiveAction):
    pass


class InstantStateAction(StateAction, InstantAction):
    pass

