from typing import Type, Callable, Any, Coroutine

from VegansDeluxe.core.Events.Events import GameEvent, Event

HandlerType = Callable[..., Coroutine]


class EventSubscription:
    def __init__(self,
                 session_id: str,
                 handler:  HandlerType,
                 event: Type[Event],
                 max_repeats: int = -1,
                 min_wait_turns: int = 0,
                 unique_type: Any = None,
                 priority: int = 0,
                 filters=None):

        if filters is None:
            filters = []
        self.session_id = session_id

        self.handler:  HandlerType = handler
        self.event_type: Type[Event] = event
        self.max_repeats = max_repeats
        self.times_executed = set()
        self.unique_type = unique_type
        self.priority = priority

        self.min_wait_turns = min_wait_turns
        self.turns_waited = set()

        self.filters: list[Callable] = filters

    def is_valid_turn(self, event: Event) -> bool:
        if not isinstance(event, GameEvent):
            return self.is_valid_event(event)
        if self.min_wait_turns > len(self.turns_waited):
            self.turns_waited.add(event.turn)
            return False
        if self.max_repeats != -1 and len(self.times_executed) >= self.max_repeats:
            if event.turn not in self.times_executed:
                return False
        return True

    def is_valid_event(self, event: Event) -> bool:
        if isinstance(event, GameEvent) and event.session_id != self.session_id:
            return False
        return isinstance(event, self.event_type) and event.unique_type == self.unique_type

    def is_valid_filter(self, message: Event) -> bool:
        return all(map(lambda f: f(message), self.filters))

    async def handle(self, event: Event):
        if not self.is_valid_turn(event):
            return False
        if not self.is_valid_event(event):
            return False
        if not self.is_valid_filter(event):
            return False

        if isinstance(event, GameEvent):
            self.times_executed.add(event.turn)

        return await self.handler(event)


class ConstantEventSubscription(EventSubscription):
    def __init__(self, session_id: str, handler:  HandlerType):
        super().__init__(session_id, handler, event=Event)


class ScheduledEventSubscription(EventSubscription):
    def __init__(self,
                 session_id: str,
                 handler:  HandlerType,
                 event: Type[Event],
                 start: int,
                 interval: int,
                 max_repeats: int = -1,
                 min_wait_turns: int = 0,
                 priority: int = 0,
                 filters=None
                 ):
        super().__init__(session_id, handler, event, max_repeats=max_repeats, min_wait_turns=min_wait_turns,
                         priority=priority, filters=filters)
        self.start = start
        self.interval = interval

    def is_valid_schedule(self, message: GameEvent) -> bool:
        if message.turn < self.start:
            return False
        if self.interval != 0:
            return (message.turn - self.start) % self.interval == 0
        else:
            return message.turn == self.start

    def handle(self, message: Event):
        if not isinstance(message, GameEvent) or self.is_valid_schedule(message):
            super().handle(message)


class SingleTurnHandler(ScheduledEventSubscription):
    def __init__(self, session_id: str, handler:  HandlerType, event: Type[Event], turn: int, priority: int = 0,
                 filters=None):
        super().__init__(session_id, handler, event, start=turn, interval=0, max_repeats=1, priority=priority,
                         filters=filters)
