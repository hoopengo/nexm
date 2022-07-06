from dataclasses import dataclass

import pytest
from nexm import Market


@dataclass
class Interaction:
    id: int


some_inter = Interaction(123)


def test_get():
    store = Market(some_inter)
    assert store.get("NotFound") is None
    assert store.get("_id") == some_inter.id

    store.clean()


def test_set():
    store = Market(some_inter)

    store.set("key", "value")

    store.clean()


def test_remove():
    store = Market(some_inter)

    assert store.remove("NotFound") is False

    store.set("key", "value")

    assert store.remove("key")

    store.clean()


def test_update_interaction():
    store = Market(some_inter)
    store.set("some_val", 123)

    new_inter = Interaction(321)

    store.update_interaction(new_inter)
    assert store.get("some_val") == 123
    assert store.get("_id") == 321

    store.clean()


def test_clean():
    store = Market(some_inter)
    store.clean()


def test_check_valid():
    store = Market(some_inter)

    try:
        store.set("", "value")
    except ValueError:
        pass
    except Exception:
        pytest.fail("Unexpected error")

    try:
        store.set(128, "value")
    except TypeError:
        pass
    except Exception:
        pytest.fail("Unexpected error")

    store.clean()
