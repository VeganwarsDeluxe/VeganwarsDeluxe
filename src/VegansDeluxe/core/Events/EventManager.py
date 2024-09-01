import threading
from apscheduler.schedulers.background import BackgroundScheduler

from VegansDeluxe.core.Events.Events import GameEvent, Event
from VegansDeluxe.core.Events.EventHandlers import EventHandler, ScheduledEventHandler, SingleTurnHandler

from typing import Callable, Type, Awaitable, Any


class EventManager:
    def __init__(self):
        self._handlers: list[EventHandler] = []

    @property
    def size(self):
        return len(self._handlers)

    def clean_by_session_id(self, session_id: str):
        self._handlers = list(filter(lambda eh: eh.session_id != session_id, self._handlers))

    async def publish_and_get_responses(self, event: Event):
        responses = []

        self._handlers.sort(key=lambda h: h.priority)
        for handler in self._handlers:
            if isinstance(event, GameEvent) and event.session_id != handler.session_id:
                continue
            response = await handler(event)
            responses.append(response)
        return responses

    def every(self,
              callback_wrapper:  Callable[[Any, Any], Awaitable[Any]],
              session_id: str,
              turns: int,
              start: int = 1,
              event: Type[Event] = Event,
              filters=None):

        handler = ScheduledEventHandler(session_id, callback_wrapper, event, start=start, interval=turns,
                                        max_repeats=-1, filters=filters)
        self._handlers.append(handler)

    def at(self,
           callback_wrapper:  Callable[[Any, Any], Awaitable[Any]],
           session_id: str,
           turn: int,
           event: Type[Event] = Event,
           priority: int = 0,
           filters=None):

        handler = SingleTurnHandler(session_id, callback_wrapper, event, turn=turn, priority=priority, filters=filters)
        self._handlers.append(handler)

    def nearest(self,
                callback_wrapper:  Callable[[Any, Any], Awaitable[Any]],
                session_id: str,
                event: Type[Event] = Event,
                priority=0,
                filters=None):

        handler = EventHandler(session_id, callback_wrapper, event, max_repeats=1, priority=priority, filters=filters)
        self._handlers.append(handler)

    def after(self,
              callback_wrapper:  Callable[[Any, Any], Awaitable[Any]],
              session_id: str,
              turns: int,
              event: Type[Event] = Event,
              repeats: int = 1,
              filters=None):

        handler = EventHandler(session_id, callback_wrapper, event, max_repeats=repeats, min_wait_turns=turns,
                               filters=filters)
        self._handlers.append(handler)

    def at_event(self,
                 callback_wrapper:  Callable[[Any, Any], Awaitable[Any]],
                 session_id: str = None,
                 event: Type[Event] = Event,
                 unique_type=None,
                 priority=0,
                 filters=None):

        handler = EventHandler(session_id, callback_wrapper, event,
                               unique_type=unique_type, priority=priority, filters=filters)
        self._handlers.append(handler)
