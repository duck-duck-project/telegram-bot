import pytest

from services.text import parse_abbreviated_number


@pytest.mark.parametrize(
    'number, expected',
    [
        ('1k', 1_000),
        ('1к', 1_000),
        ('1кк', 1_000_000),
        ('1kk', 1_000_000),
        ('10kk', 10_000_000),
    ],
)
def test_parse_abbreviated_number(number, expected):
    assert parse_abbreviated_number(number) == expected


def test_parse_abbreviated_number_empty():
    with pytest.raises(ValueError) as error:
        parse_abbreviated_number('')
    assert str(error.value) == 'Number is empty'


@pytest.mark.parametrize(
    'number',
    [
        'k1',
        'к1',
        'k',
        'к',
    ],
)
def test_parse_abbreviated_number_not_start_with_digit(number):
    with pytest.raises(ValueError) as error:
        parse_abbreviated_number(number)
    assert str(error.value) == 'Number does not start with a digit'
