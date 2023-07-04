from core import Singleton
from core.Actions.Action import Action
from core.Actions.WeaponAction import WeaponAction
from core.Actions.StateAction import StateAction
from core.Entities.Entity import Entity
from core.Events.EventManager import EventManager
from core.Events.Events import CallActionsGameEvent, AttachSessionEvent
from core.Actions import ItemAction
from core.Items.Item import Item
from core.SessionManager import SessionManager
from core.Sessions import Session
from typing import Union

from core.States import State
from core.Weapons import Weapon

ActionOwnerType = Union[type[Entity], type[Weapon], type[State], type[Item]]


class ActionManager(Singleton):
    def __init__(self):
        self.action_queue: list[Action] = []
        self.item_queue: list[ItemAction] = []

        self.all_actions: dict[ActionOwnerType, list[type[Action]]] = {}
        self.actions: dict[tuple[Session, Entity], list[Action]] = {}
        self.session_manager = SessionManager()
        self.event_manager = EventManager()

        @self.event_manager.at_event(event=AttachSessionEvent)
        def func(event: AttachSessionEvent):
            self.register(event.session_id)

    # Decorator
    def register_action(self, cls: ActionOwnerType):
        def decorator_func(action: type[Action]):
            if cls not in self.all_actions:
                self.all_actions.update({cls: []})
            self.all_actions[cls].append(action)
            return action

        return decorator_func

    def update_actions(self, session: Session):
        for entity in session.entities:
            entity_actions = self.actions[(session, entity)]
            entity_actions.clear()

            entity_type = type(entity)
            if entity_type in self.all_actions:
                for action in self.all_actions[entity_type]:
                    action: type[Action]
                    entity_actions.append(action(session, entity))

            weapon_type = type(entity.weapon)
            if weapon_type in self.all_actions:
                for action in self.all_actions[weapon_type]:
                    action: type[WeaponAction]
                    entity_actions.append(action(session, entity, entity.weapon))

            for state in entity.skills:
                state_type = type(state)
                if state_type in self.all_actions:
                    for action in self.all_actions[state_type]:
                        action: type[StateAction]
                        entity_actions.append(action(session, entity, state))

            for item in entity.items:
                item_type = type(item)
                if item_type in self.all_actions:
                    for action in self.all_actions[item_type]:
                        action: type[ItemAction]
                        entity_actions.append(action(session, entity, item))

    def get_action(self, session: Session, entity: Entity, action_id: str):
        return list(filter(lambda a: action_id == a.id, self.actions[(session, entity)]))[0]

    def queue_action(self, session: Session, entity: Entity, action_id: str) -> bool:
        action: Action = self.get_action(session, entity, action_id)
        self.action_queue.append(action)
        return not action.cost

    def register(self, session_id):
        @self.event_manager.at_event(session_id, event=CallActionsGameEvent)
        def func(event: CallActionsGameEvent):
            for action in self.action_queue:
                if action.session.id != session_id:
                    continue
                action()
            self.action_queue.clear()


action_manager = ActionManager()
AttachedAction = action_manager.register_action
