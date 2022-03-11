from pystdlib.literals import Chars


def test_char_accent():
    assert Chars.ACCENT == "^"


def test_char_ampersand():
    assert Chars.AMPERSAND == "&"


def test_char_arrows_left():
    assert Chars.ARROWS_LEFT == "«"


def test_char_arrows_right():
    assert Chars.ARROWS_RIGHT == "»"


def test_char_asterisk():
    assert Chars.ASTERISK == "*"


# noinspection SpellCheckingInspection
def test_char_atsign():
    """
    The at sign character (@).

    :return: the at sign character (@)
    """
    assert Chars.ATSIGN == "@"


def test_char_backslash():
    assert Chars.BACKSLASH == "\\"


def test_char_bitcoin():
    assert Chars.BITCOIN == "₿"


def test_char_cents():
    assert Chars.CENTS == "¢"


def test_char_colon():
    assert Chars.COLON == ":"


def test_char_comma():
    assert Chars.COMMA == ","


def test_char_copyright():
    assert Chars.COPYRIGHT == "©"


def test_char_dollar():
    assert Chars.DOLLAR == "$"


def test_char_dot():
    assert Chars.DOT == "."


# noinspection SpellCheckingInspection
def test_char_dquote():
    assert Chars.DQUOTE == "\""


def test_char_ellipsis():
    assert Chars.ELLIPSIS == "…"


def test_char_empty_braces():
    assert Chars.EMPTY_BRACES == "{}"


def test_char_empty_brackets():
    assert Chars.EMPTY_BRACKETS == "[]"


# noinspection SpellCheckingInspection
def test_char_empty_dquotes():
    assert Chars.EMPTY_DQUOTES == "\"\""


def test_char_empty_parens():
    assert Chars.EMPTY_PARENS == "()"


# noinspection SpellCheckingInspection
def test_char_empty_squotes():
    assert Chars.EMPTY_SQUOTES == "''"


def test_char_equals():
    assert Chars.EQUALS == "="


def test_char_euro():
    assert Chars.EURO == "€"


def test_char_exclamation():
    assert Chars.EXCLAMATION == "!"


# noinspection SpellCheckingInspection
def test_char_forwardslash():
    assert Chars.FORWARDSLASH == "/"


def test_char_frac_hlf():
    assert Chars.FRAC_HLF == "½"


def test_char_frac_qtr():
    assert Chars.FRAC_QTR == "¼"


def test_char_frac_3qtr():
    assert Chars.FRAC_3QTR == "¾"


def test_char_greater_than():
    assert Chars.GREATER_THAN == ">"


def test_char_greater_than_equal():
    assert Chars.GREATER_THAN_EQUAL == "≥"


def test_char_hash():
    assert Chars.HASH == "#"


def test_char_hyphen():
    assert Chars.HYPHEN == "-"


def test_char_less_than():
    assert Chars.LESS_THAN == "<"


def test_char_less_than_equal():
    assert Chars.LESS_THAN_EQUAL == "≤"


def test_char_micro():
    assert Chars.MICRO == "μ"


def test_char_minus():
    assert Chars.MINUS == "-"


def test_char_negative_one():
    assert Chars.NEGATIVE_ONE == "-1"


def test_char_not_equal():
    assert Chars.NOT_EQUAL == "≠"


def test_char_one():
    assert Chars.ONE == "1"


def test_char_paragraph():
    assert Chars.PARAGRAPH == "¶"


def test_char_percent():
    assert Chars.PERCENT == "%"


def test_char_plus():
    assert Chars.PLUS == "+"


def test_char_plus_minus():
    assert Chars.PLUS_MINUS == "±"


def test_char_pound():
    assert Chars.POUND == "£"


def test_char_power():
    assert Chars.POWER == "⏻"


def test_char_question():
    assert Chars.QUESTION == "?"


def test_char_registered():
    assert Chars.REGISTERED == "®"


def test_char_semicolon():
    assert Chars.SEMICOLON == ";"


def test_char_space():
    assert Chars.SPACE == " "


def test_char_squote():
    assert Chars.SQUOTE == "'"


def test_char_tab():
    assert Chars.TAB == "\t"


def test_char_tilde():
    assert Chars.TILDE == "~"


def test_char_trademark():
    assert Chars.TRADEMARK == "™"


def test_char_underscore():
    assert Chars.UNDERSCORE == "_"


def test_char_vertical():
    assert Chars.VERTICAL == "|"


def test_char_yen():
    assert Chars.YEN == "¥"


def test_char_zero():
    assert Chars.ZERO == "0"
