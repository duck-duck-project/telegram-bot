import pytest

from services.text import render_units


@pytest.mark.parametrize("units, decimal_points_shift, expected", [
    (100, 2, '1 ед.'),
    (123, 2, '1,23 ед.'),
    (120, 2, '1,2 ед.'),
    (125, 2, '1,25 ед.'),
    (1234567890, 2, '12345678,9 ед.'),
    (-123, 2, '-1,23 ед.'),
    (0, 2, '0 ед.'),
    (123, 3, '0,123 ед.'),
    (123, 5, '0,00123 ед.'),
    (123456, 3, '123,456 ед.'),
    (12345678, 6, '12,345678 ед.'),
    (12345, 2, '123,45 ед.')
])
def test_render_units(units, decimal_points_shift, expected):
    assert render_units(units, decimal_points_shift) == expected
