import json

import pytest

from clyde.models.locale import Locale


@pytest.mark.parametrize('value', Locale.__members__.values())
def test_is_valid(value):
    assert Locale.is_valid(value)
    assert Locale.is_valid(value.value)

@pytest.mark.parametrize('value', [
    'en',
    'spanish',
    35,
    True,
    3.14,
    [],
    'ENGLISH',
    'French',
    'Locale.DE',
    None,
])
def test_is_not_valid(value):
    assert not Locale.is_valid(value)


@pytest.mark.parametrize('locale', Locale.__members__.values())
def test_dumps(locale):
    assert json.dumps(locale) == '"' + locale.value + '"'
