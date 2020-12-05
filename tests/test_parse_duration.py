import pytest
import datetime

from helpers import parse_duration


def test_examples():
    assert parse_duration("1 week 2 days") == datetime.timedelta(days=7 + 2)
    assert parse_duration("1 month 2 weeks") == datetime.timedelta(days=30 + 2 * 7)
    assert parse_duration("12 hours") == datetime.timedelta(hours=12)

    assert parse_duration("1 hour 8 days") == datetime.timedelta(hours=1, days=8)
    assert parse_duration("1 hours 8 days") == datetime.timedelta(hours=1, days=8)

    with pytest.raises(ValueError):
        parse_duration("1 hour 2 hour")

    with pytest.raises(ValueError):
        parse_duration("1 invalidunit")

    with pytest.raises(ValueError):
        parse_duration("1 invalidunits")

    with pytest.raises(ValueError):
        parse_duration("hour 2")

    with pytest.raises(ValueError):
        parse_duration("2hours")

    with pytest.raises(ValueError):
        parse_duration("2 hours 3")

    with pytest.raises(ValueError):
        parse_duration("-2 hours")

    assert parse_duration("24 hours") == parse_duration("1 day")


def test_simple_durations():
    assert parse_duration("1 month") == datetime.timedelta(days=30)
    assert parse_duration("2 month") == datetime.timedelta(days=2 * 30)
    assert parse_duration("1 months") == datetime.timedelta(days=30)
    assert parse_duration("2 months") == datetime.timedelta(days=2 * 30)

    assert parse_duration("1 week") == datetime.timedelta(days=7)
    assert parse_duration("2 week") == datetime.timedelta(days=14)
    assert parse_duration("1 weeks") == datetime.timedelta(days=7)
    assert parse_duration("2 weeks") == datetime.timedelta(days=14)

    assert parse_duration("1 hour") == datetime.timedelta(hours=1)
    assert parse_duration("2 hour") == datetime.timedelta(hours=2)
    assert parse_duration("1 hours") == datetime.timedelta(hours=1)
    assert parse_duration("2 hours") == datetime.timedelta(hours=2)

    assert parse_duration("1 day") == datetime.timedelta(days=1)
    assert parse_duration("2 day") == datetime.timedelta(days=2)
    assert parse_duration("1 days") == datetime.timedelta(days=1)
    assert parse_duration("2 days") == datetime.timedelta(days=2)

    assert parse_duration("1 year") == datetime.timedelta(days=1 * 365)
    assert parse_duration("2 year") == datetime.timedelta(days=2 * 365)
    assert parse_duration("1 years") == datetime.timedelta(days=1 * 365)
    assert parse_duration("2 years") == datetime.timedelta(days=2 * 365)


def test_composite():
    assert parse_duration("27 years 3 month 78 weeks 12 days 314 hours") == datetime.timedelta(
        days=27 * 365 + 3 * 30 + 78 * 7 + 12, hours=314
    )
