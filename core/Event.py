class Event:
    def __init__(self):
        self.event = []

        self.action = None
        self.item = None

    def end(self):
        if self.event:
            self.event.pop(-1)

    def now(self, event):
        self.event.append(event)

    @property
    def depth(self):
        return len(self.event)

    @property
    def moment(self):
        return self.event[-1] if self.event else None

    def __str__(self):
        return "$".join(self.event)
