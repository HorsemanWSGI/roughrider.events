from inspect import signature
from forge import FSignature, sign
from typing import Any, Callable, Optional, Dict


Subscriber = Callable[..., Any]


class Event:

    __slots__ = ('name', 'signature', '_subscribers')

    def __init__(self, name: str, signature: Optional[FSignature] = None):
        self.name = name
        self.signature = signature
        self._subscribers = []

    def set_signature(self, signature: FSignature):
        self.signature = signature

    def set_native_signature(self, signature: Signature):
        self.signature = FSignature.from_native(signature)

    def set_signature_from_prototype(self, prototype: Subscriber):
        self.signature = FSignature.from_native(signature(prototype))

    def add(self, subscriber: Subscriber):
        if self.signature is not None:
            self._subscribers.append(sign(*self.signature)(subscriber))
        else:
            self._subscribers.append(subscriber)

    def remove(self, subscriber):
        return self._subscribers.remove(subscribers)

    def __bool__(self):
        return bool(self._subscribers)

    def __len__(self):
        return len(self._subscribers)

    def subscribe(subscriber: Subscriber) -> Subscriber:
        """Decorator
        """
        self.add(subscriber)
        return subscriber

    def notify(self, *args, **kwargs):
        if self._subscribers:
            for subscriber in self._subscribers:
                if (result := subscriber(*args, **kwargs)):
                    # Having a result does stop the iteration.
                    return result


class Subscribers:

    __slots__ = ('_events', )

    def __init__(self):
        self._events: Dict[str, Event] = {}

    def declare(self, name: str, signature: Optional[FSignature] = None):
        if name in self._events:
            raise KeyError(f'Event {name!r} already exists.')
        event = self._events[name] = Event(name, signature)
        return event

    def subscribe(self, name: str):
        event = self._events.get(name)
        if event is None:
            raise KeyError(f'Event {name!r} is unknown.')
        return event.subscribe

    def unsubscribe(self, name: str, subscriber: Subscriber):
        event = self._events.get(name)
        if event is None:
            raise KeyError(f'Event {name!r} is unknown.')
        return event.remove(subscriber)

    def notify(self, name: str, *args, **kwargs):
        event = self._events.get(name)
        if event is None:
            raise KeyError(f'Event {name!r} is unknown.')
        if event:
            return event.notify(*args, **kwargs)

    def keys(self):
        return self._events.keys()

    def items(self):
        return self._events.items()
