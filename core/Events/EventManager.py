from core import Singleton
from core.Events.Events import GameEvent, Event, AttachStateEvent
from core.Events.EventHandlers import EventHandler, ScheduledEventHandler, SingleTurnHandler, ConstantEventHandler
from core.States import State

from typing import Callable, Type


class EventManager(Singleton):
    def __init__(self):
        self._handlers: list[EventHandler] = []

    def publish(self, event: Event):
        self._handlers.sort(key=lambda h: h.priority)
        for handler in self._handlers:
            if isinstance(event, GameEvent) and event.session_id != handler.session_id:
                continue
            handler(event)
        return event

    def every(self, session_id: str, turns: int, start: int = 1, event: Type[Event] = Event, filters=None):
        def decorator_func(callback: Callable):
            handler = ScheduledEventHandler(session_id, callback, event, start=start, interval=turns, max_repeats=-1,
                                            filters=filters)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def at(self, session_id: str, turn: int, event: Type[Event] = Event, priority: int = 0, filters=None):
        def decorator_func(callback: Callable):
            handler = SingleTurnHandler(session_id, callback, event, turn=turn, priority=priority, filters=filters)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def nearest(self, session_id: str, event: Type[Event] = Event, priority=0, filters=None):
        def decorator_func(callback: Callable):
            handler = EventHandler(session_id, callback, event, max_repeats=1, priority=priority, filters=filters)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def after(self, session_id: str, turns: int, event: Type[Event] = Event, repeats: int = 1, filters=None):
        def decorator_func(callback: Callable):
            handler = EventHandler(session_id, callback, event, max_repeats=repeats, min_wait_turns=turns,
                                   filters=filters)
            self._handlers.append(handler)
            return callback

        return decorator_func

    def at_event(self, callback_wrapper, session_id: str = None, event: Type[Event] = Event, unique_type=None,
                 priority=0, filters=None):
        handler = EventHandler(session_id, callback_wrapper, event, unique_type=unique_type, priority=priority,
                               filters=filters)
        self._handlers.append(handler)

    def constantly(self, session_id: str):
        def decorator_func(callback: Callable):
            handler = ConstantEventHandler(session_id, callback)
            self._handlers.append(handler)
            return callback

        return decorator_func


event_manager = EventManager()
