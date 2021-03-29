from reiter.events.meta import EventsCenter
from reiter.events.dispatcher import Dispatcher


class Application(EventsCenter):
    pass


class Item:
    def __init__(self, _type):
        self._type = _type


class ItemTypeDispatcher(Dispatcher):

    def dispatch(self, item, **kwargs):
        return item._type


def test_no_dispatch():
    app = Application()
    mc = ItemTypeDispatcher()

    app.subscribe('object_added')(mc)
    app.notify('object_added', Item('car'))


def test_dispatch():
    app = Application()
    mc = ItemTypeDispatcher()
    app.subscribe('object_added')(mc)

    found = []

    @mc.subscribe('car')
    def only_for_car(item, **kwargs):
        found.append('I have a car.')

    assert list(mc.dispatch_keys) == ['car']

    app.notify('object_added', Item('bus'))
    assert found == []

    app.notify('object_added', Item('car'))
    assert found == ['I have a car.']
