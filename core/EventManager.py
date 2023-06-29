from typing import Type
from core import Singleton
from core.Event import Event


class EventManager(Singleton):
    def __init__(self):
        self._handlers: list[Handler] = []

    def every(self, session_id, turns: int, start: int = 1, events: Type[Event] = Event):
        """
        @session.handlers.every(session_id, 2, events='post-attack')
        def func(message):
            self.owner.say('I say this every 2 turns at post-attack!')
        """

        def decorator_func(func):
            self._handlers.append(
                ScheduledHandler(session_id, func, events, start=start, interval=turns, repeats=-1)
            )
            return func

        return decorator_func

    def at(self, session_id, turn, event=Event):
        def decorator_func(func):
            self._handlers.append(
                SingleTurnHandler(session_id, func, event, turn)
            )
            return func

        return decorator_func

    def now(self, session_id, event=Event):
        def decorator_func(func):
            self._handlers.append(
                Handler(session_id, func, event, repeats=1)
            )
            return func

        return decorator_func

    def at_event(self, session_id, event=Event):
        def decorator_func(func):
            self._handlers.append(
                Handler(session_id, func, event)
            )
            return func

        return decorator_func

    def constantly(self, session_id):
        def decorator_func(func):
            self._handlers.append(
                Handler(session_id, func, Event)
            )
            return func

        return decorator_func

    def publish(self, message: Event):
        for handler in self._handlers:
            handler(message)


class Handler:
    def __init__(self, session_id, func, events: Type[Event], repeats=-1):
        self.session_id = session_id

        self.func = func
        self.event: Type[Event] = events
        self.repeats = repeats
        self.times_executed = set()

    def is_triggered(self, message: Event):
        if message.session_id != self.session_id:
            return False
        if self.repeats != -1 and len(self.times_executed) >= self.repeats:
            if message.turn not in self.times_executed:
                return False
        return self.is_event_triggered(message)

    def is_event_triggered(self, message):
        return isinstance(message, self.event)

    def __call__(self, message):
        if self.is_triggered(message):
            self.func(message)
            self.times_executed.add(message.turn)


class ConstantHandler(Handler):
    def __init__(self, session_id, func):
        super().__init__(session_id, func, events=Event)


class ScheduledHandler(Handler):
    def __init__(self, session_id, func, events, start, interval, repeats=-1):
        super().__init__(session_id, func, events, repeats=repeats)

        self.start = start
        self.interval = interval

    def check_turn(self, message):
        if message.turn < self.start:
            return
        return (message.turn - self.start) % self.interval == 0

    def __call__(self, message):
        if not self.check_turn(message):
            return
        super().__call__(message)


class SingleTurnHandler(ScheduledHandler):
    def __init__(self, session_id, func, events, turn):
        super().__init__(session_id, func, events, start=turn, interval=1, repeats=1)
