from core.TimeMomentStack import TimeMomentStack


class EventManager:
    def __init__(self):
        self.handlers: list[Handler] = []

        self.time_stack: TimeMomentStack = TimeMomentStack()

    def every(self, turns, start=1, events=True):
        """
        @session.handlers.every(2, events='post-attack')
        def func(message):
            self.owner.say('I say this every 2 turns at post-attack!')
        """

        def decorator_func(func):
            self.handlers.append(
                ScheduledHandler(func, events, start=start, interval=turns, repeats=-1)
            )
            return func

        return decorator_func

    def at(self, turn, events=True):
        def decorator_func(func):
            self.handlers.append(
                SingleTurnHandler(func, events, turn)
            )
            return func

        return decorator_func

    def now(self, events=True):
        def decorator_func(func):
            self.handlers.append(
                Handler(func, events, repeats=1)
            )
            return func

        return decorator_func

    def at_event(self, events=True):
        def decorator_func(func):
            self.handlers.append(
                Handler(func, events)
            )
            return func

        return decorator_func

    def constantly(self):
        def decorator_func(func):
            self.handlers.append(
                Handler(func, True)
            )
            return func

        return decorator_func

    def publish(self, message):
        self.time_stack.start(message.current_event)

        self.trigger_handlers(message)

        self.time_stack.end()

    def trigger_handlers(self, message):
        for handler in self.handlers:
            handler(message)


class Handler:
    def __init__(self, func, events, repeats=-1):
        self.func = func
        self.events = events

        self.repeats = repeats
        self.last_executed = 0
        self.times_executed = set()

    def is_triggered(self, message):
        if self.repeats != -1 and len(self.times_executed) >= self.repeats:
            if message.turn not in self.times_executed:
                return False
        return self.is_event_triggered(message)

    def is_event_triggered(self, message):
        if self.events is True:
            return True
        if message.current_event == self.events:
            return True
        return False

    def __call__(self, message):
        if self.is_triggered(message):
            self.func(message)

            self.last_executed = message.turn
            self.times_executed.add(message.turn)


class ConstantHandler(Handler):
    def __init__(self, func):
        super().__init__(func, events=True)


class ScheduledHandler(Handler):
    def __init__(self, func, events, start, interval, repeats=-1):
        super().__init__(func, events, repeats=repeats)

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
    def __init__(self, func, events, turn):
        super().__init__(func, events, start=turn, interval=1, repeats=1)
