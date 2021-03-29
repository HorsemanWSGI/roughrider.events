from dataclasses import dataclass, field


@dataclass
class EventsCenter:
    subscribers: dict = field(default_factory=registries.Subscribers)

    def subscribe(self, *args, **kwargs):
        return self.subscribers.subscribe(*args, **kwargs)

    def notify(self, *args, **kwargs):
        return self.subscribers.notify(*args, **kwargs)
