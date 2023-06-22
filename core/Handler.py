from typing import Union


class HandlerManager:
    def __init__(self, session):
        self.session = session
        self.handlers: list[Handler] = []

    def every(self, turns, start=1, events=True):
        """
        @session.handlers.every(2, events='post-attack')
        def func():
            self.owner.say('I say this every 2 turns at post-attack!')
        """

        def decorator_func(func):
            self.handlers.append(
                ScheduledHandler(self.session, func, events, start=start, interval=turns, repeats=-1)
            )
            return func

        return decorator_func

    def at(self, turn, events=True):
        def decorator_func(func):
            self.handlers.append(
                SingleTurnHandler(self.session, func, events, turn)
            )
            return func

        return decorator_func

    def at_event(self, events=True):
        def decorator_func(func):
            self.handlers.append(
                Handler(self.session, func, events)
            )
            return func

    def constantly(self):
        def decorator_func(func):
            self.handlers.append(
                Handler(self.session, func, True)
            )
            return func

        return decorator_func

    def event(self):
        for handler in self.handlers:
            handler()


class Handler:
    def __init__(self, session, func, events, repeats=-1):
        self.session = session
        self.func = func
        self.events = events

        self.repeats = repeats
        self.last_executed = 0
        self.times_executed = set()

    def is_triggered(self):
        if self.events is True:
            return True
        if self.session.current_stage not in self.events:
            return False
        if self.repeats != -1:
            if len(self.times_executed) >= self.repeats:
                return False
        if self.events == self.session.current_stage:
            return True

    def __call__(self):
        if self.is_triggered():
            self.func()

            self.last_executed = self.session.turn
            self.times_executed.add(self.session.turn)


class ConstantHandler(Handler):
    def __init__(self, session, func):
        super().__init__(session, func, events=True)


class ScheduledHandler(Handler):
    def __init__(self, session, func, events, start, interval, repeats=-1):
        super().__init__(session, func, events, repeats=repeats)

        self.start = start
        self.interval = interval

    def check_turn(self):
        return (self.session.turn - self.start) % self.interval == 0

    def __call__(self):
        if self.check_turn():
            super().__call__()


class SingleTurnHandler(ScheduledHandler):
    def __init__(self, session, func, events, turn):
        super().__init__(session, func, events, turn, 1, 1)
