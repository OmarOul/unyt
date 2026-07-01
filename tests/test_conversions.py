from unyt.units import UNITS
from unyt.main import affine_transformation, inverse_affine_transformation, convert

import pytest

def test_affine_identity():
    # scale=1, offset=0 should return the value unchanged
    assert affine_transformation(5.0, 1.0, 0.0) == 5.0

def test_inverse_affine_identity():
    assert inverse_affine_transformation(5.0, 1.0, 0.0) == 5.0

def test_affine_and_inverse_are_symmetric():
    # applying affine then its inverse should return the original value
    scale, offset = 5/9, (5/9) * 459.67
    result = inverse_affine_transformation(
                affine_transformation(100.0, scale, offset),
                scale, offset
             )
    assert abs(result - 100.0) < 1e-9

@pytest.mark.parametrize("start, end, value, expected", [
    # Temperature
    ("celsius", "fahrenheit", 0.0, 32.0),
    ("celsius", "fahrenheit", 100.0, 212.0),
    ("celsius", "kelvin", 0.0, 273.15),
    # Length
    ("km", "meters", 1.0, 1000.0),
    ("feet", "meters", 1.0, 0.3048),
    ("miles", "meters", 1.0, 1609.344),
    # Mass
    ("g", "kg", 1000.0, 1.0),
])
def test_fixed_points(start, end, value, expected):
    assert convert(start, end, value) == pytest.approx(expected)

def test_temp_roundtrip():
    # the inverse of a conversion should take us to the starting point.
    result_a = convert("celsius", "fahrenheit", 0.0)
    result_b = convert("fahrenheit", "celsius", result_a)
    assert result_b ==pytest.approx(0.0)
