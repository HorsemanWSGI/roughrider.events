import multidict
import itertools
from typing import Callable


class Subscribers(multidict.MultiDict):

    def __add__(self, subdict: multidict.MultiDict):
        return self.__class__(
            itertools.chain(self.items(), subdict.items()))

    def subscribe(self, name: str):
        def add_subscriber(subscriber: Callable) -> Callable:
            self.add(name, subscriber)
            return subscriber
        return add_subscriber

    def notify(self, name: str, *args, **kwargs):
        if name in self:
            for subscriber in self.getall(name):
                if (result := subscriber(*args, **kwargs)):
                    # Having a result does stop the iteration.
                    return result
