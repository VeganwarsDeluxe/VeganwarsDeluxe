from core.Events.Events import GameEvent, Event
from core.Events.EventHandlers import EventHandler, ScheduledEventHandler, SingleTurnHandler, ConstantEventHandler

from typing import Callable, Type


class EventManager:
    def __init__(self):
        self._handlers: list[EventHandler] = []

    def clean_by_session_id(self, session_id: str):
        self._handlers = list(filter(lambda eh: eh.session_id == session_id, self._handlers))

    def publish(self, event: Event):
        self._handlers.sort(key=lambda h: h.priority)
        for handler in self._handlers:
            if isinstance(event, GameEvent) and event.session_id != handler.session_id:
                continue
            handler(event)
        return event

    def every(self,
              callback_wrapper: Callable,
              session_id: str,
              turns: int,
              start: int = 1,
              event: Type[Event] = Event,
              filters=None):

        handler = ScheduledEventHandler(session_id, callback_wrapper, event, start=start, interval=turns,
                                        max_repeats=-1, filters=filters)
        self._handlers.append(handler)

    def at(self,
           callback_wrapper: Callable,
           session_id: str,
           turn: int,
           event: Type[Event] = Event,
           priority: int = 0,
           filters=None):

        handler = SingleTurnHandler(session_id, callback_wrapper, event, turn=turn, priority=priority, filters=filters)
        self._handlers.append(handler)

    def nearest(self,
                callback_wrapper: Callable,
                session_id: str,
                event: Type[Event] = Event,
                priority=0,
                filters=None):

        handler = EventHandler(session_id, callback_wrapper, event, max_repeats=1, priority=priority, filters=filters)
        self._handlers.append(handler)

    def after(self,
              callback_wrapper: Callable,
              session_id: str,
              turns: int,
              event: Type[Event] = Event,
              repeats: int = 1,
              filters=None):

        handler = EventHandler(session_id, callback_wrapper, event, max_repeats=repeats, min_wait_turns=turns,
                               filters=filters)
        self._handlers.append(handler)

    def at_event(self,
                 callback_wrapper: Callable,
                 session_id: str = None,
                 event: Type[Event] = Event,
                 unique_type=None,
                 priority=0,
                 filters=None):

        handler = EventHandler(session_id, callback_wrapper, event,
                               unique_type=unique_type, priority=priority, filters=filters)
        self._handlers.append(handler)
