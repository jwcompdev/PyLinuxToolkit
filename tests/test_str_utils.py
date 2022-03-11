import pytest

from pystdlib.str_utils import *
from pystdlib.utils import IllegalArgumentError


def test_is_boolean():
    assert is_boolean("true")
    assert is_boolean("false")
    assert is_boolean("t")
    assert is_boolean("f")
    assert is_boolean("1")
    assert is_boolean("0")
    assert is_boolean("succeed")
    assert is_boolean("fail")
    assert is_boolean("succeeded")
    assert is_boolean("failed")
    assert is_boolean("yes")
    assert is_boolean("no")
    assert is_boolean("enabled")
    assert is_boolean("disabled")
    assert is_boolean("y")
    assert is_boolean("n")
    assert is_boolean("TRUE")
    assert is_boolean(" FALSE ")
    assert is_boolean("FALSE ")
    assert is_boolean(" FALSE")
    assert not is_boolean(" FALSE /")
    assert not is_boolean(" !@#$%^&*() ")
    assert not is_boolean("")
    # noinspection PyTypeChecker
    assert not is_boolean(None)


def test_to_boolean():
    assert to_boolean("true")
    assert not to_boolean("false")
    assert to_boolean("t")
    assert not to_boolean("f")
    assert to_boolean("1")
    assert not to_boolean("0")
    assert to_boolean("succeed")
    assert not to_boolean("fail")
    assert to_boolean("succeeded")
    assert not to_boolean("failed")
    assert to_boolean("yes")
    assert not to_boolean("no")
    assert to_boolean("enabled")
    assert not to_boolean("disabled")
    assert to_boolean("y")
    assert not to_boolean("n")
    assert to_boolean("TRUE")
    assert not to_boolean(" FALSE ")
    assert not to_boolean("FALSE ")
    assert not to_boolean(" FALSE")
    assert to_boolean(" FALSE /") is None
    assert to_boolean(" !@#$%^&*() ") is None
    assert to_boolean("") is None
    # noinspection PyTypeChecker
    assert to_boolean(None) is None


def test_parse_int_test_no_match():
    with pytest.raises(ValueError):
        parse_int("")
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        parse_int(None)
    with pytest.raises(ValueError):
        parse_int("abcd")
    with pytest.raises(ValueError):
        parse_int("1.0")


def test_parse_int_test_no_match_with_default():
    assert parse_int("", 1) == 1
    # noinspection PyTypeChecker
    assert parse_int(None, 1) == 1
    assert parse_int("abcd", 1) == 1
    assert parse_int("1.0", 1) == 1
    # noinspection PyTypeChecker
    assert parse_int(None, 1.5) == 1
    assert parse_int("abcd", 1.0) == 1

    assert parse_int("", 2) == 2
    # noinspection PyTypeChecker
    assert parse_int(None, 2) == 2
    assert parse_int("abcd", 2) == 2
    assert parse_int("1.0", 2) == 2

    assert isinstance(parse_int("", 2), int)
    assert isinstance(parse_int("", 2.0), int)

    with pytest.raises(ValueError):
        parse_int("", None)
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        parse_int(None, None)
    with pytest.raises(ValueError):
        parse_int("abcd", None)
    with pytest.raises(ValueError):
        parse_int("1.0", None)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        parse_int("", [])
    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        parse_int(None, "")


def test_parse_int_test_match():
    assert parse_int("1") == 1
    assert parse_int("0") == 0
    assert parse_int("50") == 50
    assert parse_int("100") == 100


def test_parse_int_test_match_with_default():
    assert parse_int("1", 5) == 1
    assert parse_int("0", 1) == 0
    assert parse_int("50", 1) == 50
    assert parse_int("100", 1) == 100


def test_parse_float_test_no_match():
    with pytest.raises(ValueError):
        parse_float("")
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        parse_float(None)
    with pytest.raises(ValueError):
        parse_float("abcd")


def test_parse_float_test_no_match_with_default():
    assert parse_float("", 2.8) == 2.8
    # noinspection PyTypeChecker
    assert parse_float(None, 1.5) == 1.5
    assert parse_float("abcd", 1.0) == 1.0

    assert parse_float("", 2) == 2
    # noinspection PyTypeChecker
    assert parse_float(None, 2) == 2
    assert parse_float("abcd", 2) == 2

    assert isinstance(parse_float("", 2), float)
    assert isinstance(parse_float("", 2.0), float)

    with pytest.raises(ValueError):
        parse_float("", None)
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        parse_float(None, None)
    with pytest.raises(ValueError):
        parse_float("abcd", None)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        parse_float("", [])
    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        parse_float(None, "")


def test_parse_float_test_match():
    assert parse_float("1") == 1.0
    assert parse_float("0") == 0.0
    assert parse_float("50") == 50.0
    assert parse_float("100") == 100.0


def test_parse_float_test_match_with_default():
    assert parse_float("1", 5) == 1.0
    assert parse_float("0", 1) == 0.0
    assert parse_float("50", 1) == 50.0
    assert parse_float("100", 1) == 100.0


def test_is_blank():
    assert is_blank("")
    assert is_blank("     ")
    assert not is_blank("abcd")
    assert not is_blank(" 1234 ")
    assert not is_blank("!@#$%^&*()_+")
    # noinspection PyTypeChecker
    assert not is_blank(None)


def test_is_not_blank():
    assert not is_not_blank("")
    assert not is_not_blank("     ")
    assert is_not_blank("abcd")
    assert is_not_blank(" 1234 ")
    assert is_not_blank("!@#$%^&*()_+")
    # noinspection PyTypeChecker
    assert is_not_blank(None)


def test_is_blank_or_none():
    assert is_blank_or_none("")
    assert is_blank_or_none("     ")
    assert not is_blank_or_none("abcd")
    assert not is_blank_or_none(" 1234 ")
    assert not is_blank_or_none("!@#$%^&*()_+")
    # noinspection PyTypeChecker
    assert is_blank_or_none(None)


def test_is_not_blank_or_none():
    assert not is_not_blank_or_none("")
    assert not is_not_blank_or_none("     ")
    assert is_not_blank_or_none("abcd")
    assert is_not_blank_or_none(" 1234 ")
    assert is_not_blank_or_none("!@#$%^&*()_+")
    # noinspection PyTypeChecker
    assert not is_not_blank_or_none(None)


def test_wrap():
    assert wrap("Hello World!", '*') == "*Hello World!*"

    assert wrap("Hello World!", '') == "Hello World!"

    assert wrap("World", ' Hello ') == " Hello World Hello "

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        wrap(None, None)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        wrap(1, 1)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        wrap("", None)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        wrap(None, "")


def test_unwrap_success():
    assert unwrap("*Hello World!*", '*') == "Hello World!"

    assert unwrap(" Hello World Hello ", " Hello ") == "World"


def test_unwrap_failure():
    assert unwrap("*Hello World!", '*') == "*Hello World!"

    assert unwrap("Hello World!*", '*') == "Hello World!*"

    assert unwrap("Hello World!", '*') == "Hello World!"

    assert unwrap(" Hello World", " Hello ") == " Hello World"

    assert unwrap("World Hello ", " Hello ") == "World Hello "

    assert unwrap("Hello World", " Hello ") == "Hello World"

    assert unwrap("World", " Hello ") == "World"

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        unwrap(None, None)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        unwrap(1, 1)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        unwrap("", None)

    with pytest.raises(IllegalArgumentError):
        # noinspection PyTypeChecker
        unwrap(None, "")


def test_uuid():
    assert uuid(seed=1234) == "1de9ea66-70d3-4a1f-8735-df5ef7697fb9"
    assert uuid(False, seed=1234) == "1de9ea66-70d3-4a1f-8735-df5ef7697fb9"
    assert uuid(True, seed=1234) == "1de9ea6670d34a1f8735df5ef7697fb9"
    assert uuid(as_hex=True, seed=1234) == "1de9ea6670d34a1f8735df5ef7697fb9"
    assert uuid(True, 1234) == "1de9ea6670d34a1f8735df5ef7697fb9"
    assert uuid(False) != "1de9ea66-70d3-4a1f-8735-df5ef7697fb9"
    assert uuid(True) != "1de9ea6670d34a1f8735df5ef7697fb9"
    assert uuid(False, None) != "1de9ea66-70d3-4a1f-8735-df5ef7697fb9"
    assert uuid(True, None) != "1de9ea6670d34a1f8735df5ef7697fb9"


def test_random_string():
    assert random_string(5, seed=1234) == "9XCha"
    assert random_string(9, seed=1234) == "9XChaf688"
    assert random_string(5, seed=1111) == "nmwWP"
    assert random_string(5, seed=123) == "drfXA"
    assert random_string(5, seed=0) == "2yW4A"

    assert random_string(9, seed=None) != "9XChaf688"

    with pytest.raises(IllegalArgumentError):
        random_string(-1)


def test_reverse():
    assert reverse("hello") == "olleh"
    assert reverse("Hello World!") == "!dlroW olleH"
    assert reverse("12345") == "54321"
    assert reverse("") == ""
    assert reverse("1") == "1"

    with pytest.raises(InvalidInputError):
        # noinspection PyTypeChecker
        reverse(None)
