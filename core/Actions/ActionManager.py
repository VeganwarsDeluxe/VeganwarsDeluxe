import typing
from typing import Union

from core.Decorators import RegisterEvent
from core.Actions.Action import Action
from core.Actions.ItemAction import ItemAction
from core.Actions.StateAction import StateAction
from core.Actions.WeaponAction import WeaponAction
from core.Context import StateContext, EventContext
from core.Entities.Entity import Entity
from core.Events.EventManager import event_manager
from core.Events.Events import CallActionsGameEvent, AttachSessionEvent, PreMoveGameEvent, PostUpdateActionsGameEvent, \
    PreUpdateActionsGameEvent
from core.Items.Item import Item
from core.SessionManager import SessionManager
from core.Sessions import Session
from core.States import State
from core.Weapons import Weapon

ActionOwnerType = Union[type[Entity], type[Weapon], type[State], type[Item]]

from collections import defaultdict


class ActionManager:
    def __init__(self):
        self.action_queue: list[Action] = []
        self.all_actions: dict[ActionOwnerType, list[type[Action]]] = defaultdict(list)
        self.actions: dict[tuple[Session, Entity], list[Action]] = {}
        self.session_manager = SessionManager()

        @RegisterEvent(event=AttachSessionEvent)
        def handle_attach_session(context: EventContext[AttachSessionEvent]):
            self.register(context.session.id)

        @RegisterEvent(event=PreMoveGameEvent)
        def handle_pre_move_game_event(context: EventContext[PreMoveGameEvent]):
            self.reset_removed_actions(context.session.id)

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

    def attach_action(self, session: Session, entity: Entity, action_id: str):
        owner_type, action_type = self.get_action_from_all_actions(action_id)
        if isinstance(owner_type, Entity):
            action = action_type(session, entity)
        else:
            action = action_type(session, entity, owner_type())
        self.actions[(session, entity)].append(action)

    def update_entity_actions(self, session: Session, entity: Entity):
        event_manager.publish(PreUpdateActionsGameEvent(session.id, session.turn, entity.id))

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

        event_manager.publish(PostUpdateActionsGameEvent(session.id, session.turn, entity.id))

    def update_actions(self, session: Session):
        for entity in session.entities:
            self.update_entity_actions(session, entity)

    def get_action(self, session: Session, entity: Entity, action_id: str):
        actions = filter(lambda a: action_id == a.id, self.get_actions(session, entity))
        return next(actions, None)

    def get_action_from_all_actions(self, action_id: str) -> \
            typing.Optional[tuple[type[ActionOwnerType], type[Action]]]:
        for action_owner in self.all_actions:
            for action in self.all_actions[action_owner]:
                if action.id == action_id:
                    return action_owner, action

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

    def is_action_available(self, session: Session, entity: Entity, action_id: str) -> bool:
        for action in self.get_available_actions(session, entity):
            if action.id == action_id:
                return True
        return False

    def get_queued_entity_actions(self, session: Session, entity: Entity) -> list[Action]:
        result = []
        for action in self.get_queued_session_actions(session):
            if action.source != entity:
                continue
            result.append(action)
        return result

    def get_queued_session_actions(self, session: Session) -> list[Action]:
        queue = [action for action in self.action_queue if action.session.id == session.id]
        return queue

    def remove_action(self, session: Session, entity: Entity, action_id: str):
        action = self.get_action(session, entity, action_id)
        if action:
            action.removed = True
        return action

    def queue_action(self, session: Session, entity: Entity, action_id: str) -> bool:
        action: Action = self.get_action(session, entity, action_id)
        return self.queue_action_instance(action)

    def queue_action_instance(self, action: Action) -> bool:
        self.action_queue.append(action)
        return not action.cost

    def register(self, session_id):
        @RegisterEvent(session_id, event=CallActionsGameEvent)
        def handle_call_actions_game_event(context: EventContext[CallActionsGameEvent]):
            action_queue = [action for action in self.action_queue if action.session.id == session_id]
            action_queue.sort(key=lambda a: a.priority)
            for action in action_queue:
                action()
                self.action_queue.remove(action)


action_manager = ActionManager()
AttachedAction = action_manager.register_action
