import pytest

from pystdlib.condition import Condition


def test_condition_bool():
    assert Condition(True).result is True
    assert Condition(False).result is False

    assert Condition(True, True, True).result is True
    assert Condition(False, False, False).result is False

    assert Condition(True, False, False).result is False
    assert Condition(False, True, False).result is False
    assert Condition(False, False, True).result is False
    assert Condition(True, True, False).result is False
    assert Condition(False, True, True).result is False
    assert Condition(True, False, True).result is False


def test_condition_collections():
    assert Condition((True, True, True)).result is True
    assert Condition((False, False, False)).result is False

    assert Condition([True, True, True]).result is True
    assert Condition([False, False, False]).result is False

    assert Condition({True, True, True}).result is True
    assert Condition({False, False, False}).result is False

    assert Condition({1: True, 2: True, 3: True}).result is True
    assert Condition({1: False, 2: False, 3: False}).result is False


def test_condition_use_not():
    assert Condition(True, use_not=True).result is False
    assert Condition(False, use_not=True).result is True

    assert Condition(True, True, True, use_not=True).result is False
    assert Condition(False, False, False, use_not=True).result is True

    assert Condition(True, False, False, use_not=True).result is False
    assert Condition(False, True, False, use_not=True).result is False
    assert Condition(False, False, True, use_not=True).result is False
    assert Condition(True, True, False, use_not=True).result is False
    assert Condition(False, True, True, use_not=True).result is False
    assert Condition(True, False, True, use_not=True).result is False


def test_condition_use_or():
    assert Condition(True, use_or=True).result is True
    assert Condition(False, use_or=True).result is False

    assert Condition(True, True, True, use_or=True).result is True
    assert Condition(False, False, False, use_or=True).result is False

    assert Condition(True, False, False, use_or=True).result is True
    assert Condition(False, True, False, use_or=True).result is True
    assert Condition(False, False, True, use_or=True).result is True
    assert Condition(True, True, False, use_or=True).result is True
    assert Condition(False, True, True, use_or=True).result is True
    assert Condition(True, False, True, use_or=True).result is True


def test_ignore_invalid():
    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        _ = Condition(None).result

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        _ = Condition(None, ignore_invalid=True).result

    with pytest.raises(ValueError):
        # noinspection PyTypeChecker
        _ = Condition(None, True).result

    # noinspection PyTypeChecker
    assert Condition(None, True, ignore_invalid=True).result is True
    # noinspection PyTypeChecker
    assert Condition(None, False, ignore_invalid=True).result is False


def test_condition_evaluate():
    assert Condition(True).evaluate().result is True
    assert Condition(False).evaluate().result is False

    assert Condition(True).evaluate(False).result is False
    assert Condition(False).evaluate(False).result is False
    assert Condition(True).evaluate(True).result is True
    assert Condition(False).evaluate(True).result is False

    assert Condition(True).evaluate([False]).result is False
    assert Condition(True).evaluate({False}).result is False
    assert Condition(True).evaluate({1: True}).result is True
    assert Condition(True).evaluate((True,)).result is True

    assert Condition(True).evaluate(True).evaluate(False).result is False


def test_condition_evaluate_lazy():
    assert Condition(True, lazy=False).result is True
    assert Condition(True, lazy=True).result is None
    assert Condition(True, lazy=True).evaluate().result is True


def test_condition_ifs():
    assert Condition(True).is_true() is True
    assert Condition(True).is_false() is False
    assert Condition(True).get() is True

    result = None

    def True_Func():
        """True Func."""
        nonlocal result
        result = True

    def False_Func():
        """False Func."""
        nonlocal result
        result = False

    Condition(True).if_true(True_Func)
    assert result is True

    result = None
    Condition(False).if_false(False_Func)
    assert result is False

    result = None
    Condition(True).if_false(True_Func)
    assert result is None

    result = None
    Condition(False).if_true(False_Func)
    assert result is None


def test_condition_raise():
    with pytest.raises(ValueError):
        Condition(False).raise_if_false(ValueError, "FALSE")

    with pytest.raises(ValueError):
        Condition(True).raise_if_true(ValueError, "TRUE")

    with pytest.raises(RuntimeError):
        Condition(False).raise_if_false(RuntimeError, "FALSE")

    Condition(True).raise_if_false(RuntimeError, "FALSE")
    Condition(False).raise_if_true(RuntimeError, "TRUE")
