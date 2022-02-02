from datetime import datetime, timezone

import pytest

from clyde.models.snowflake import Snowflake

SNOWFLAKES = [
    Snowflake(175928847299117063),
    Snowflake('175928847299117063'),
]


def test_out_of_bounds_init_int():
    with pytest.raises(ValueError):
        _ = Snowflake(-12345)  # Negative value

    with pytest.raises(ValueError):
        _ = Snowflake(2 ** 65)  # Value too large for uint64


def test_out_of_bounds_init_str():
    with pytest.raises(ValueError):
        _ = Snowflake('-12345')  # Negative value

    with pytest.raises(ValueError):
        _ = Snowflake('36893488147419103232')  # Value too large for uint64

    with pytest.raises(ValueError):
        _ = Snowflake('')  # Empty string


def test_invalid_init_types():
    with pytest.raises(TypeError):
        _ = Snowflake(None)  # NoneType is invalid

    with pytest.raises(TypeError):
        _ = Snowflake([])  # list is invalid

    with pytest.raises(TypeError):
        _ = Snowflake({})  # dict is invalid

    with pytest.raises(TypeError):
        _ = Snowflake(3.14159)  # float is invalid (should not be rounded)


def test_equality():
    assert Snowflake(175928847299117063) == Snowflake(175928847299117063)
    assert Snowflake(175928847299117063) == Snowflake('175928847299117063')
    assert Snowflake('175928847299117063') == Snowflake(175928847299117063)
    assert Snowflake('175928847299117063') == Snowflake('175928847299117063')


def test_inequality():
    assert Snowflake(175928847299117063) != Snowflake(7792287155374570356)
    assert Snowflake(175928847299117063) != Snowflake('7792287155374570356')
    assert Snowflake('175928847299117063') != Snowflake(7792287155374570356)
    assert Snowflake('175928847299117063') != Snowflake('7792287155374570356')


@pytest.mark.parametrize('snow', SNOWFLAKES)
def test_properties(snow):
    assert snow.timestamp == 1462015105796
    assert snow.time == datetime(
        2016, 4, 30, 11, 18, 25, 796000, tzinfo=timezone.utc)
    assert snow.worker_id == 1
    assert snow.process_id == 0
    assert snow.sequence == 7


@pytest.mark.parametrize('snow', SNOWFLAKES)
def test_conversions(snow):
    assert str(snow) == '175928847299117063'  # To int
    assert int(snow) == 175928847299117063  # To str
