import uuid
from collections import defaultdict
from typing import Type

from VegansDeluxe.core.Events.EventHandlers import EventSubscription, ScheduledEventSubscription, SingleTurnSubscription
from VegansDeluxe.core.Events.EventHandlers import HandlerType
from VegansDeluxe.core.Events.Events import Event, GameEvent


class EventManager:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self._subscriptions: list[EventSubscription] = []
        self._by_event_type = defaultdict(list)
        self._by_session_and_event_type = defaultdict(lambda: defaultdict(list))


    @property
    def size(self):
        return len(self._subscriptions)

    def clean_by_session_id(self, session_id: str):
        self._subscriptions = [
            sub for sub in self._subscriptions
            if sub.session_id != session_id
        ]
        self._by_session_and_event_type.pop(session_id, None)

        # optional: rebuild global index to be safe
        self._by_event_type.clear()
        for sub in self._subscriptions:
            if sub.session_id is None:
                self._by_event_type[sub.event_type].append(sub)

    async def publish(self, event: Event):
        event_types = type(event).mro()
        session_id = event.session_id if isinstance(event, GameEvent) else None

        candidates = []
        for event_type in event_types:
            candidates.extend(self._by_event_type.get(event_type, ()))
            if session_id is not None:
                candidates.extend(
                    self._by_session_and_event_type
                    .get(session_id, {})
                    .get(event_type, ())
                )

        candidates.sort(key=lambda h: h.priority)

        responses = []
        for subscription in candidates:
            responses.append(await subscription.handle(event))
        return responses

    def add_subscription(self, subscription: EventSubscription):
        self._subscriptions.append(subscription)

        if subscription.session_id is None:
            self._by_event_type[subscription.event_type].append(subscription)
        else:
            self._by_session_and_event_type[subscription.session_id][subscription.event_type].append(subscription)

    def every(self,
              callback_wrapper: HandlerType,
              session_id: str,
              turns: int,
              start: int = 1,
              event: Type[Event] = Event,
              filters=None,
              subscription_id=None):
        subscription = ScheduledEventSubscription(session_id, callback_wrapper, event, start=start, interval=turns,
                                                  max_repeats=-1, filters=filters, subscription_id=subscription_id)
        self.add_subscription(subscription)

    def at(self,
           callback_wrapper: HandlerType,
           session_id: str,
           turn: int,
           event: Type[Event] = Event,
           priority: int = 0,
           filters=None,
           subscription_id=None):
        subscription = SingleTurnSubscription(session_id, callback_wrapper, event, turn=turn, priority=priority,
                                              filters=filters, subscription_id=subscription_id)
        self.add_subscription(subscription)

    def nearest(self,
                callback_wrapper: HandlerType,
                session_id: str,
                event: Type[Event] = Event,
                priority=0,
                filters=None,
                subscription_id=None
                ):
        handler = EventSubscription(session_id, callback_wrapper, event, max_repeats=1, priority=priority,
                                    filters=filters, subscription_id=subscription_id)
        self.add_subscription(handler)

    def after(self,
              callback_wrapper: HandlerType,
              session_id: str,
              turns: int,
              event: Type[Event] = Event,
              repeats: int = 1,
              filters=None,
              subscription_id=None
              ):
        handler = EventSubscription(session_id, callback_wrapper, event, max_repeats=repeats, min_wait_turns=turns,
                                    filters=filters, subscription_id=subscription_id)
        self.add_subscription(handler)

    def at_event(self,
                 callback_wrapper: HandlerType,
                 session_id: str = None,
                 event: Type[Event] = Event,
                 unique_type=None,
                 priority=0,
                 filters=None,
                 subscription_id=None
                 ):
        handler = EventSubscription(session_id, callback_wrapper, event,
                                    unique_type=unique_type, priority=priority, filters=filters,
                                    subscription_id=subscription_id)
        self.add_subscription(handler)
