import uuid
from typing import Type

from VegansDeluxe.core.Events.EventHandlers import EventSubscription, ScheduledEventSubscription, SingleTurnSubscription
from VegansDeluxe.core.Events.EventHandlers import HandlerType
from VegansDeluxe.core.Events.Events import GameEvent, Event


class EventManager:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self._subscriptions: list[EventSubscription] = []

    @property
    def size(self):
        return len(self._subscriptions)

    def clean_by_session_id(self, session_id: str):
        self._subscriptions = list(filter(lambda eh: eh.session_id != session_id, self._subscriptions))

    async def publish(self, event: Event):
        responses = []

        self._subscriptions.sort(key=lambda h: h.priority)
        for subscription in self._subscriptions:
            if isinstance(event, GameEvent) and event.session_id != subscription.session_id:
                continue
            response = await subscription.handle(event)
            responses.append(response)
        return responses

    def add_subscription(self, subscription: EventSubscription):
        self._subscriptions.append(subscription)

    def every(self,
              callback_wrapper: HandlerType,
              session_id: str,
              turns: int,
              start: int = 1,
              event: Type[Event] = Event,
              filters=None):

        subscription = ScheduledEventSubscription(session_id, callback_wrapper, event, start=start, interval=turns,
                                                  max_repeats=-1, filters=filters)
        self.add_subscription(subscription)

    def at(self,
           callback_wrapper: HandlerType,
           session_id: str,
           turn: int,
           event: Type[Event] = Event,
           priority: int = 0,
           filters=None):

        subscription = SingleTurnSubscription(session_id, callback_wrapper, event, turn=turn, priority=priority,
                                              filters=filters)
        self.add_subscription(subscription)

    def nearest(self,
                callback_wrapper: HandlerType,
                session_id: str,
                event: Type[Event] = Event,
                priority=0,
                filters=None):

        handler = EventSubscription(session_id, callback_wrapper, event, max_repeats=1, priority=priority,
                                    filters=filters)
        self.add_subscription(handler)

    def after(self,
              callback_wrapper: HandlerType,
              session_id: str,
              turns: int,
              event: Type[Event] = Event,
              repeats: int = 1,
              filters=None):

        handler = EventSubscription(session_id, callback_wrapper, event, max_repeats=repeats, min_wait_turns=turns,
                                    filters=filters)
        self.add_subscription(handler)

    def at_event(self,
                 callback_wrapper: HandlerType,
                 session_id: str = None,
                 event: Type[Event] = Event,
                 unique_type=None,
                 priority=0,
                 filters=None):

        handler = EventSubscription(session_id, callback_wrapper, event,
                                    unique_type=unique_type, priority=priority, filters=filters)
        self.add_subscription(handler)
