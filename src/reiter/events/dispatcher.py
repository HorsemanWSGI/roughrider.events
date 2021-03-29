from reiter.events.meta import EventsCenter


class Dispatcher(EventsCenter):

    @property
    def dispatch_keys(self):
        return self.subscribers.keys()

    def dispatch(self, *args, **kwargs):
        raise NotImplementedError('Implement your dispatcher')

    def __call__(self, *args, **kwargs):
        key = self.dispatch(*args, **kwargs)
        self.notify(key, *args, **kwargs)
