from core import Singleton
from core.Events.Events import GameEvent, Event, AttachStateEvent
from core.Events.EventHandlers import EventHandler, ScheduledEventHandler, SingleTurnHandler, ConstantEventHandler
from core.States import State

from typing import Callable, Type


class EventManager(Singleton):
    def __init__(self):
        self._handlers: list[EventHandler] = []

    def publish(self, message: Event):
        for handler in self._handlers:
            if isinstance(message, GameEvent) and message.session_id != handler.session_id:
                continue
            handler(message)

    def every(self, session_id: str, turns: int, start: int = 1, event: Type[Event] = Event):
        def decorator_func(callback: Callable):
            handler = ScheduledEventHandler(session_id, callback, event, start=start, interval=turns, max_repeats=-1)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def at(self, session_id: str, turn: int, event: Type[Event] = Event):
        def decorator_func(callback: Callable):
            handler = SingleTurnHandler(session_id, callback, event, turn=turn)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def now(self, session_id: str, event: Type[Event] = Event):
        def decorator_func(callback: Callable):
            handler = EventHandler(session_id, callback, event, max_repeats=1)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def after(self, session_id: str, turns: int, event: Type[Event] = Event, repeats: int = 1):
        def decorator_func(callback: Callable):
            handler = EventHandler(session_id, callback, event, max_repeats=repeats, min_wait_turns=turns)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def at_event(self, session_id: str = None, event: Type[Event] = Event, unique_type=None):
        def decorator_func(callback: Callable):
            handler = EventHandler(session_id, callback, event, unique_type=unique_type)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def constantly(self, session_id: str):
        def decorator_func(callback: Callable):
            handler = ConstantEventHandler(session_id, callback)
            self._handlers.append(handler)
            return callback

        return decorator_func


event_manager = EventManager()


def RegisterState(state: type[State]):
    return event_manager.at_event(event=AttachStateEvent, unique_type=state)
