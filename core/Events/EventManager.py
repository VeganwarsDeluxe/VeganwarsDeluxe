from typing import Type
from core import Singleton
from core.Events.Events import Event
from core.Events.Handlers import Handler, ScheduledHandler, SingleTurnHandler, ConstantHandler


class EventManager(Singleton):
    def __init__(self):
        self._handlers: list[Handler] = []

    def publish(self, message: Event):
        for handler in self._handlers:
            if message.session_id != handler.session_id:
                continue
            handler(message)

    def every(self, session_id, turns: int, start: int = 1, event: Type[Event] = Event):
        """
        @event_manager.every(session_id, turns=2, event=PostAttackEvent)
        def func(message: PostAttackEvent):
            self.owner.say('I say this every 2 turns at post-attack!')
        """

        def decorator_func(func):
            handler = ScheduledHandler(session_id, func, event, start=start, interval=turns, repeats=-1)
            self._handlers.append(handler)
            return func
        return decorator_func

    def at(self, session_id, turn, event=Event):
        """
        @event_manager.at(session_id, turn=5, event=DeathEvent)
        def func(message: DeathEvent):
            message.entity.say('I say this exactly at turn 5 during death event! Also, I died.')
        """

        def decorator_func(func):
            handler = SingleTurnHandler(session_id, func, event, turn)
            self._handlers.append(handler)
            return func

        return decorator_func

    def now(self, session_id, event=Event):
        def decorator_func(func):
            handler = Handler(session_id, func, event, repeats=1)
            self._handlers.append(handler)
            return func

        return decorator_func

    def after(self, session_id, turns, event=Event, repeats=1):
        def decorator_func(func):
            handler = Handler(session_id, func, event, repeats=repeats, wait_for=turns)
            self._handlers.append(handler)
            return func

        return decorator_func

    def at_event(self, session_id, event=Event):
        def decorator_func(func):
            handler = Handler(session_id, func, event)
            self._handlers.append(handler)
            return func

        return decorator_func

    def constantly(self, session_id):
        def decorator_func(func):
            handler = ConstantHandler(session_id, func)
            self._handlers.append(handler)
            return func
        return decorator_func
