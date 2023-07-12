from typing import Union

from core import Singleton
from core.Actions.Action import Action
from core.Actions.ItemAction import ItemAction
from core.Actions.StateAction import StateAction
from core.Actions.WeaponAction import WeaponAction
from core.Entities.Entity import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import CallActionsGameEvent, AttachSessionEvent, PreMoveGameEvent
from core.Items.Item import Item
from core.SessionManager import SessionManager
from core.Sessions import Session
from core.States import State
from core.Weapons import Weapon

ActionOwnerType = Union[type[Entity], type[Weapon], type[State], type[Item]]

from collections import defaultdict


class ActionManager(Singleton):
    def __init__(self):
        self.action_queue: list[Action] = []
        self.all_actions: dict[ActionOwnerType, list[type[Action]]] = defaultdict(list)
        self.actions: dict[tuple[Session, Entity], list[Action]] = {}
        self.session_manager = SessionManager()

        @event_manager.at_event(event=AttachSessionEvent)
        def handle_attach_session(event: AttachSessionEvent):
            self.register(event.session_id)

        @event_manager.at_event(event=PreMoveGameEvent)
        def handle_pre_move_game_event(event: PreMoveGameEvent):
            self.reset_removed_actions(event.session_id)

    def register_action(self, cls: ActionOwnerType):
        def decorator_func(action: type[Action]):
            if cls not in self.all_actions:
                self.all_actions.update({cls: []})
            self.all_actions[cls].append(action)
            action.cls = cls
            return action

        return decorator_func

    def reset_removed_actions(self, session_id):
        session = self.session_manager.get_session(session_id)
        for entity in session.entities:
            entity_actions = self.actions[(session, entity)]
            for action in entity_actions:
                action.removed = False

    def update_entity_actions(self, session: Session, entity: Entity):
        entity_actions = self.actions.get((session, entity))
        if not entity_actions:
            entity_actions = []
            self.actions[(session, entity)] = entity_actions
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

    def update_actions(self, session: Session):
        for entity in session.entities:
            self.update_entity_actions(session, entity)

    def get_action(self, session: Session, entity: Entity, action_id: str):
        actions = filter(lambda a: action_id == a.id, self.get_actions(session, entity))
        return next(actions, None)

    def get_actions(self, session: Session, entity: Entity):
        return self.actions[(session, entity)]

    def get_available_actions(self, session: Session, entity: Entity):
        actions = self.get_actions(session, entity)
        result = []
        for action in actions:
            if action.removed:
                continue
            if action.hidden:
                continue
            result.append(action)
        return result

    def get_queued_entity_actions(self, session: Session, entity: Entity) -> list[Action]:
        queue = [action for action in self.action_queue if action.session.id == session.id]
        result = []
        for action in queue:
            if action.source != entity:
                continue
            result.append(action)
        return result

    def remove_action(self, session: Session, entity: Entity, action_id: str):
        actions = self.actions[(session, entity)]
        action = next((a for a in actions if a.id == action_id), None)
        if action:
            action.removed = True
        return action

    def queue_action(self, session: Session, entity: Entity, action_id: str) -> bool:
        action: Action = self.get_action(session, entity, action_id)
        self.action_queue.append(action)
        return not action.cost

    def register(self, session_id):
        @event_manager.at_event(session_id, event=CallActionsGameEvent)
        def handle_call_actions_game_event(event: CallActionsGameEvent):
            action_queue = [action for action in self.action_queue if action.session.id == session_id]
            action_queue.sort(key=lambda a: a.priority)
            for action in action_queue:
                action()
                self.action_queue.remove(action)


action_manager = ActionManager()
AttachedAction = action_manager.register_action
