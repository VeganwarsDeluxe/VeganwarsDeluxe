from typing import Type, Callable, Any

from core.Events.Events import GameEvent, Event


class EventHandler:
    def __init__(self,
                 session_id: str,
                 callback: Callable,
                 events: Type[Event],
                 max_repeats: int = -1,
                 min_wait_turns: int = 0,
                 unique_type: Any = None,
                 priority: int = 0):
        self.session_id = session_id

        self.callback = callback
        self.event_type: Type[Event] = events
        self.max_repeats = max_repeats
        self.times_executed = set()
        self.unique_type = unique_type
        self.priority = priority

        self.min_wait_turns = min_wait_turns
        self.turns_waited = set()

    def is_valid_turn(self, message: Event) -> bool:
        if not isinstance(message, GameEvent):
            return self.is_valid_event(message)
        if self.min_wait_turns > len(self.turns_waited):
            self.turns_waited.add(message.turn)
            return False
        if self.max_repeats != -1 and len(self.times_executed) >= self.max_repeats:
            if message.turn not in self.times_executed:
                return False
        return self.is_valid_event(message)

    def is_valid_event(self, message: Event) -> bool:
        return isinstance(message, self.event_type) and message.unique_type == self.unique_type

    def __call__(self, message: Event):
        if self.is_valid_turn(message):
            self.callback(message)
            if isinstance(message, GameEvent):
                self.times_executed.add(message.turn)


class ConstantEventHandler(EventHandler):
    def __init__(self, session_id: str, callback: Callable):
        super().__init__(session_id, callback, events=Event)


class ScheduledEventHandler(EventHandler):
    def __init__(self,
                 session_id: str,
                 callback: Callable,
                 events: Type[Event],
                 start: int,
                 interval: int,
                 max_repeats: int = -1,
                 min_wait_turns: int = 0):
        super().__init__(session_id, callback, events, max_repeats=max_repeats, min_wait_turns=min_wait_turns)

        self.start = start
        self.interval = interval

    def is_valid_schedule(self, message: GameEvent) -> bool:
        if message.turn < self.start:
            return False
        return (message.turn - self.start) % self.interval == 0

    def __call__(self, message: Event):
        if not isinstance(message, GameEvent) or self.is_valid_schedule(message):
            super().__call__(message)


class SingleTurnHandler(ScheduledEventHandler):
    def __init__(self, session_id: str, callback: Callable, events: Type[Event], turn: int):
        super().__init__(session_id, callback, events, start=turn, interval=1, max_repeats=1)
