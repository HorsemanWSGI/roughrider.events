import pytest
from roughrider.events.registry import Event


def test_empty_event():
    event = Event('test')
    assert event.signature is None
    assert event.name == 'test'
    assert bool(event) is False
    assert len(event) == 0
    assert event.notify() is None


def test_event_subscription():
    callstack = []
    event = Event('test')

    def my_subscriber(arg: str):
        callstack.append(arg)

    event.add(my_subscriber)
    assert bool(event) is True
    assert len(event) == 1

    # no args
    with pytest.raises(TypeError) as exc:
        event.notify()
    assert callstack == []
    assert str(exc.value) == (
        "my_subscriber() missing 1 required positional argument: 'arg'"
    )

    # proper args
    event.notify('some value')
    assert callstack == ['some value']


def test_event_subscription_signature():
    import forge
    from typing import Callable, Any


    def test(arg: str) -> Any:
        pass





    signature = forge.FSignature(
        parameters=[
            forge.pos('arg', type=str),
        ],
        return_annotation=str,
    )

    callstack = []
    event = Event('test', signature)

    def my_subscriber(arg):
        callstack.append(arg)

    event.add(my_subscriber)
    assert bool(event) is True
    assert len(event) == 1

    def other_subscriber(arg):
        callstack.append(arg)

    event.add(other_subscriber)
    assert len(event) == 2

    def faulty_subscriber(*args):
        pass

    with pytest.raises(TypeError) as exc:
        event.add(faulty_subscriber)
    assert str(exc.value) == (
        "Missing requisite mapping from parameters (arg)"
    )

    assert len(event) == 2
