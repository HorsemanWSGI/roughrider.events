from dataclasses import dataclass, field
from roughrider.events.registry import Subscribers


@dataclass
class EventsCenter:
    subscribers: dict = field(default_factory=Subscribers)

    def subscribe(self, *args, **kwargs):
        return self.subscribers.subscribe(*args, **kwargs)

    def notify(self, *args, **kwargs):
        return self.subscribers.notify(*args, **kwargs)
