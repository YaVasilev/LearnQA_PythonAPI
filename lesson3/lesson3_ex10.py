import pytest

phrase = input("Set a phrase: ")


def test_char_quantity():
    max_char_number = 15
    assert len(phrase) < max_char_number, f"The phrase is longer than {max_char_number} characters"
