import typing
from collections import defaultdict
from typing import Union

from core import Entity
from core.Actions.Action import Action
from core.Actions.ActionManager import ActionManager
from core.Context import StateContext, EventContext, ActionExecutionContext
from core.Events.Events import Event, AttachStateEvent, AttachSessionEvent, PreMoveGameEvent, CallActionsGameEvent, \
    ExecuteActionEvent, DeliveryRequestEvent, DeliveryPackageEvent
from core.Items.Item import Item
from core.States import State
from core.Weapons import Weapon

ActionOwnerType = Union[type[Entity], type[Weapon], type[State], type[Item]]


class ContentManager:
    """
    ContentManager is a singleton. It is used by content to register itself for usage
    and by Engine to retrieve the content properly.
    """

    def __init__(self):
        """
        self.action_map: Map of Content classes to Action classes.
        self.state_init_map: Map of State classes to their "game inits".
        self.assignments: List of event assignments to be completed on Engine initialization.
        self.attached_session_manager: List of attached SessionManagers.
        """
        self.action_map: dict[ActionOwnerType, list[type[Action]]] = defaultdict(list)

        self.state_init_map: dict[type[State], typing.Callable] = dict()
        self.assignments: list[typing.Callable] = list()

        self.attached_action_managers: list[ActionManager] = list()

        self.weapons: dict[str, Weapon] = dict()
        self.states: dict[str, State] = dict()
        self.items: dict[str, Item] = dict()

    def register_weapon(self, weapon: Weapon):
        self.weapons.update({weapon.id: weapon})

    def register_item(self, item: Item):
        self.items.update({item.id: item})

    def initialize_action_manager(self, action_manager: ActionManager):
        """
        On AttachSessionEvent, attaches "action calling function" to the Session.
        """

        @RegisterEvent(event=AttachSessionEvent)
        def handle_attach_session(root_context: EventContext[AttachSessionEvent]):
            @RegisterEvent(root_context.session.id, event=CallActionsGameEvent)
            def handle_call_actions_game_event(context: EventContext[CallActionsGameEvent]):
                """
                Calls all the actions in the Action Queue that attached to certain Session.
                """

                action_queue = [action for action in action_manager.action_queue
                                if action.session.id == context.session.id]
                action_queue.sort(key=lambda a: a.priority)
                for action in action_queue:
                    event = ExecuteActionEvent(context.session.id, context.session.turn, action)
                    context.event_manager.publish(event)

                    action_manager.action_queue.remove(action)

            @RegisterEvent(root_context.session.id, event=DeliveryRequestEvent)
            def handle_delivery_request(context: EventContext[DeliveryRequestEvent]):
                event = DeliveryPackageEvent(context.session.id, context.session.turn)
                context.event_manager.publish(event)

            @self.register_action_execution_event(root_context.session.id)
            def execute_action_handler(context: ActionExecutionContext):
                context.action()

        """
        Every PreMoveGameEvent, resets removed actions for the Session.
        """

        @RegisterEvent(event=PreMoveGameEvent)
        def handle_pre_move_game_event(context: EventContext[PreMoveGameEvent]):
            action_manager.reset_removed_actions(context.session.id)

    def attach_action_manager(self, action_manager: ActionManager):
        self.attached_action_managers.append(action_manager)
        for assignment in self.assignments:
            assignment(action_manager)
        for state in content_manager.state_init_map:
            content_manager.initialize_state_attachment(state, action_manager)

    def add_assignment(self, assignment: typing.Callable):
        self.assignments.append(assignment)
        for action_manager in self.attached_action_managers:
            assignment(action_manager)

    def register_event(self, session_id: str = None, event: type[Event] = Event, unique_type=None,
                       priority=0, filters=None):
        """
        Works same as self.register_state, but more complicated. Adds an Assignment to be completed
        in Engine init.
        """

        def decorator_func(callback: typing.Callable):
            def assignment(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return callback(context)

                event_manager.at_event(event=event, session_id=session_id, unique_type=unique_type,
                                       priority=priority, filters=filters, callback_wrapper=callback_wrapper)

            self.add_assignment(assignment)

        return decorator_func

    def register_action_execution_event(self, session_id: str = None, unique_type=None,
                                        priority=0, filters=None):
        """
        Works same as self.register_state, but more complicated. Adds an Assignment to be completed
        in Engine init.
        """

        def decorator_func(callback: typing.Callable):
            def assignment(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                def callback_wrapper(message):
                    context = ActionExecutionContext[
                        ExecuteActionEvent
                    ](message, session_manager.get_session(message.session_id), action_manager)
                    return callback(context)

                event_manager.at_event(event=ExecuteActionEvent, session_id=session_id, unique_type=unique_type,
                                       priority=priority, filters=filters, callback_wrapper=callback_wrapper)

            self.add_assignment(assignment)

        return decorator_func

    def register_state(self, state: type[State]):
        self.states.update({state.id: state})

        def decorator_func(callback: typing.Callable):
            """
            We actually do nothing here, we only save Callback along with the State to be
            initialized later in self.initialize_state_attachment.
            """
            self.state_init_map.update({state: callback})

        return decorator_func

    def at(self, session_id: str, turn: int, event: type[Event] = Event, priority: int = 0, filters=None):
        def decorator_func(callback: typing.Callable):
            def assignment(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return callback(context)

                event_manager.at(callback_wrapper, session_id, turn, event, priority=priority, filters=filters)

            self.add_assignment(assignment)

        return decorator_func

    def nearest(self, session_id: str, event: type[Event] = Event, priority=0, filters=None):
        def decorator_func(callback: typing.Callable):
            def assignment(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return callback(context)

                event_manager.nearest(callback_wrapper, session_id, event=event, priority=priority, filters=filters)

            self.add_assignment(assignment)

        return decorator_func

    def every(self, session_id: str, turns: int, start: int = 1, event: type[Event] = Event, filters=None):
        def decorator_func(callback: typing.Callable):
            def assignment(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return callback(context)

                event_manager.every(callback_wrapper, session_id, turns, start, event, filters)

            self.add_assignment(assignment)

        return decorator_func

    def after(self, session_id: str, turns: int, event: type[Event] = Event, repeats: int = 1, filters=None):
        def decorator_func(callback: typing.Callable):
            def assignment(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return callback(context)

                event_manager.after(event=event, session_id=session_id, turns=turns, repeats=repeats,
                                    filters=filters, callback_wrapper=callback_wrapper)

            self.add_assignment(assignment)

        return decorator_func

    def initialize_state_attachment(self, state: type[State], action_manager: ActionManager):
        """
        This method should be called when initializing new Engine.
        """
        callback = self.state_init_map[state]
        session_manager = action_manager.session_manager
        event_manager = session_manager.event_manager

        def callback_wrapper(event):
            session = session_manager.get_session(event.session_id)
            context = StateContext[state](event, session, action_manager)
            return callback(context)

        event_manager.at_event(event=AttachStateEvent, unique_type=state, callback_wrapper=callback_wrapper)

    def register_action(self, cls: ActionOwnerType):
        """
        cls: Entity, Weapon, State or Item. Action is being attached to it.
        action: Any Action.
        """

        def decorator_func(action: type[Action]):
            if cls not in self.action_map:
                self.action_map.update({cls: []})
            self.action_map[cls].append(action)
            action.cls = cls
            return action

        return decorator_func


content_manager = ContentManager()
AttachedAction = content_manager.register_action
RegisterState = content_manager.register_state
RegisterEvent = content_manager.register_event
At = content_manager.at
Nearest = content_manager.nearest
Every = content_manager.every
After = content_manager.after

RegisterWeapon = content_manager.register_weapon
RegisterItem = content_manager.register_item
