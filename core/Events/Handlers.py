from typing import Type

from core.Events import Event


class Handler:
    def __init__(self, session_id, func, events: Type[Event], repeats=-1, wait_for=0):
        self.session_id = session_id

        self.func = func
        self.event: Type[Event] = events
        self.repeats = repeats
        self.times_executed = set()

        self.wait_for = wait_for
        self.turns_waited = set()

    def turn_check(self, message: Event):
        if self.wait_for > len(self.turns_waited):
            self.turns_waited.add(message.turn)
            return False
        if self.repeats != -1 and len(self.times_executed) >= self.repeats:
            if message.turn not in self.times_executed:
                return False
        return self.event_check(message)

    def event_check(self, message):
        return isinstance(message, self.event)

    def __call__(self, message):
        if self.turn_check(message):
            self.func(message)
            self.times_executed.add(message.turn)


class ConstantHandler(Handler):
    def __init__(self, session_id, func):
        super().__init__(session_id, func, events=Event)


class ScheduledHandler(Handler):
    def __init__(self, session_id, func, events, start, interval, repeats=-1, wait_for=0):
        super().__init__(session_id, func, events, repeats=repeats, wait_for=wait_for)

        self.start = start
        self.interval = interval

    def plan_check(self, message):
        if message.turn < self.start:
            return
        return (message.turn - self.start) % self.interval == 0

    def __call__(self, message):
        if self.plan_check(message):
            super().__call__(message)


class SingleTurnHandler(ScheduledHandler):
    def __init__(self, session_id, func, events, turn):
        super().__init__(session_id, func, events, start=turn, interval=1, repeats=1)
