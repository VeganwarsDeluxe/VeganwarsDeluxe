import typing
from collections import defaultdict

from VegansDeluxe.core import Entity
from VegansDeluxe.core.Actions.Action import Action
from VegansDeluxe.core.Actions.ActionManager import ActionManager
from VegansDeluxe.core.Context import StateContext, EventContext, ActionExecutionContext
from VegansDeluxe.core.Events.Events import (Event, AttachStateEvent, AttachSessionEvent, PreMoveGameEvent,
                                             CallActionsGameEvent, ExecuteActionEvent, DeliveryRequestEvent,
                                             DeliveryPackageEvent, PostActionsGameEvent)
from VegansDeluxe.core.Items.Item import Item
from VegansDeluxe.core.States import State
from VegansDeluxe.core.Weapons import Weapon

ActionOwnerType = type[Entity] | type[Weapon] | type[State] | type[Item]


class Assignment:
    def __init__(self, func: typing.Callable, desc: str = ""):
        self.desc: str = desc
        self.func: typing.Callable = func

    def execute(self, am: ActionManager):
        return self.func(am)

    def __str__(self):
        return self.desc


class ContentManager:
    """
    ContentManager is a singleton. It is used by content to register itself for usage
    and by Engine to retrieve the content properly.
    """

    def __init__(self):
        self.action_map: dict[ActionOwnerType, list[type[Action]]] = defaultdict(list)
        """Map of Content classes to Action classes."""

        self.state_init_map: dict[type[State], typing.Callable] = dict()
        """Map of State classes to their "game inits"."""
        self.assignments: list[Assignment] = list()
        """List of event assignments to be completed on Engine initialization."""

        self.attached_action_managers: list[ActionManager] = list()
        """List of attached SessionManagers."""

        self.weapons: dict[str, Weapon] = dict()
        """Map of Weapon classes to their IDs."""
        self.states: dict[str, State] = dict()
        """Map of State classes to their IDs."""
        self.items: dict[str, Item] = dict()
        """Map of Item classes to their IDs."""

        self.add_assignment(Assignment(self.initialize_action_manager))

    def get_state(self, state_id: str) -> typing.Optional[State]:
        """
        Retrieve a state by its ID.
        If no state is found, return an empty state.
        """
        return self.states.get(state_id, State)

    def get_weapon(self, weapon_id: str) -> typing.Optional[Weapon]:
        """
        Retrieve a weapon by its ID.
        If no weapon is found, return an empty weapon.
        """
        return self.weapons.get(weapon_id, Weapon)

    def register_weapon(self, weapon: Weapon):
        self.weapons.update({weapon.id: weapon})
        return weapon

    def register_item(self, item: Item):
        self.items.update({item.id: item})
        return item

    def initialize_action_manager(self, action_manager: ActionManager):
        """
        On AttachSessionEvent, attaches "action calling function" to the Session.
        """

        @RegisterEvent(event=AttachSessionEvent)
        async def handle_attach_session(root_context: EventContext[AttachSessionEvent]):
            @RegisterEvent(root_context.session.id, event=PostActionsGameEvent, priority=99)
            async def handle_post_actions_game_event(context: EventContext[PostActionsGameEvent]):
                """
                Clears out all action from the queue after they are executed.
                :todo: Make sure if this is the right time to clear. Though before we cleared them after the execution,
                    so I think we are fine for now.
                """

                action_manager.action_queue = \
                    [action for action in action_manager.action_queue if action.session.id != root_context.session.id]

            @RegisterEvent(root_context.session.id, event=CallActionsGameEvent)
            async def handle_call_actions_game_event(context: EventContext[CallActionsGameEvent]):
                """
                Calls all the actions in the Action Queue that attached to certain Session.
                """

                action_queue = [action for action in action_manager.action_queue
                                if action.session.id == context.session.id]
                action_queue.sort(key=lambda a: a.priority)
                for action in action_queue:
                    event = ExecuteActionEvent(context.session.id, context.session.turn, action)
                    await context.event_manager.publish(event)

            @RegisterEvent(root_context.session.id, event=DeliveryRequestEvent)
            async def handle_delivery_request(context: EventContext[DeliveryRequestEvent]):
                """
                Broadcasts EventContext[DeliveryPackageEvent] immediately on receiving DeliveryRequestEvent.

                Useful to get the ActionManager contained in the EventContext, circumventing circular dependencies.
                """
                event = DeliveryPackageEvent(context.session.id, context.session.turn)
                await context.event_manager.publish(event)

            @self.register_action_execution_event(root_context.session.id)
            async def execute_action_handler(context: ActionExecutionContext):
                """Execute the action on receiving ExecuteActionEvent."""
                await context.action.execute()

        @RegisterEvent(event=PreMoveGameEvent)
        async def handle_pre_move_game_event(context: EventContext[PreMoveGameEvent]):
            """
            Every PreMoveGameEvent, resets removed actions for the Session.
            """
            action_manager.reset_removed_actions(context.session.id)

    def attach_action_manager(self, action_manager: ActionManager):
        self.initialize_action_manager(action_manager)
        self.attached_action_managers.append(action_manager)
        for assignment in self.assignments:
            assignment.execute(action_manager)
        for state in content_manager.state_init_map:
            content_manager.initialize_state_attachment(state, action_manager)

    def add_assignment(self, assignment: Assignment):
        self.assignments.append(assignment)
        self.propagate_assignment(assignment)

    def propagate_assignment(self, assignment: Assignment):
        for action_manager in self.attached_action_managers:
            assignment.execute(action_manager)

    def register_event(self, session_id: str = None, event: type[Event] = Event, unique_type=None,
                       priority=0, filters=None, subscription_id: str | None = None, add_assignment=False):
        """
        Works same as self.register_state, but more complicated. Adds an Assignment to be completed
        in Engine init.
        """

        def decorator_func(callback: typing.Callable):
            def assignment_func(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                async def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return await callback(context)

                event_manager.at_event(event=event, session_id=session_id, unique_type=unique_type,
                                       priority=priority, filters=filters, callback_wrapper=callback_wrapper,
                                       subscription_id=subscription_id)

            desc = f"RegisterEvent Assignment for session[{session_id}], event[{event}]."
            assignment = Assignment(assignment_func, desc)
            if add_assignment:
                self.add_assignment(assignment)
            else:
                self.propagate_assignment(assignment)

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

                async def callback_wrapper(message):
                    context = ActionExecutionContext[ExecuteActionEvent](
                        message, session_manager.get_session(message.session_id), action_manager
                    )
                    return await callback(context)

                event_manager.at_event(event=ExecuteActionEvent, session_id=session_id, unique_type=unique_type,
                                       priority=priority, filters=filters, callback_wrapper=callback_wrapper)

            desc = f"RegisterActionExecutionEvent Assignment for session[{session_id}], unique_type[{unique_type}]."
            self.add_assignment(Assignment(assignment, desc))

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

    def at(self, session_id: str, turn: int, event: type[Event] = Event, priority: int = 0, filters=None,
           add_assignment: bool = False):
        def decorator_func(callback: typing.Callable):
            def assignment_func(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                async def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return await callback(context)

                event_manager.at(callback_wrapper, session_id, turn, event, priority=priority, filters=filters)

            desc = f"At Assignment for session[{session_id}], unique_type[{event}]."
            assignment = Assignment(assignment_func, desc)
            if add_assignment:
                self.add_assignment(assignment)
            else:
                self.propagate_assignment(assignment)

        return decorator_func

    def next(self, session_id: str, event: type[Event] = Event, priority=0, filters=None, add_assignment: bool = False):
        def decorator_func(callback: typing.Callable):
            def assignment_func(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                async def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return await callback(context)

                event_manager.nearest(callback_wrapper, session_id, event=event, priority=priority, filters=filters)

            desc = f"Next Assignment for session[{session_id}], unique_type[{event}]."
            assignment = Assignment(assignment_func, desc)
            if add_assignment:
                self.add_assignment(assignment)
            else:
                self.propagate_assignment(assignment)

        return decorator_func

    def every(self, session_id: str, turns: int, start: int = 1, event: type[Event] = Event, filters=None,
              add_assignment: bool = False):
        def decorator_func(callback: typing.Callable):
            def assignment_func(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                async def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return await callback(context)

                event_manager.every(callback_wrapper, session_id, turns, start, event, filters)

            desc = f"Every Assignment for session[{session_id}], unique_type[{event}]."
            assignment = Assignment(assignment_func, desc)
            if add_assignment:
                self.add_assignment(assignment)
            else:
                self.propagate_assignment(assignment)

        return decorator_func

    def after(self, session_id: str, turns: int, event: type[Event] = Event, repeats: int = 1, filters=None,
              add_assignment: bool = False):
        def decorator_func(callback: typing.Callable):
            def assignment_func(action_manager: ActionManager):
                session_manager = action_manager.session_manager
                event_manager = session_manager.event_manager

                async def callback_wrapper(message):
                    context = EventContext[event](message, session_manager.get_session(message.session_id),
                                                  action_manager)
                    return await callback(context)

                event_manager.after(event=event, session_id=session_id, turns=turns, repeats=repeats,
                                    filters=filters, callback_wrapper=callback_wrapper)

            desc = f"After Assignment for session[{session_id}], unique_type[{event}]."
            assignment = Assignment(assignment_func, desc)
            if add_assignment:
                self.add_assignment(assignment)
            else:
                self.propagate_assignment(assignment)

        return decorator_func

    def initialize_state_attachment(self, state: type[State], action_manager: ActionManager):
        """
        This method should be called when initializing new Engine.
        """
        callback = self.state_init_map[state]
        session_manager = action_manager.session_manager
        event_manager = session_manager.event_manager

        async def callback_wrapper(event):
            session = session_manager.get_session(event.session_id)
            context = StateContext[state](event, session, action_manager)
            return await callback(context)

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
# Content handlers
AttachedAction = content_manager.register_action
RegisterState = content_manager.register_state
RegisterWeapon = content_manager.register_weapon
RegisterItem = content_manager.register_item

# Both
RegisterEvent = content_manager.register_event
At = content_manager.at
Next = content_manager.next
Every = content_manager.every
After = content_manager.after


