from datetime import datetime

from main import _can_run_now, _wait_until_run_time


def test_can_run_now_within_window_on_allowed_day():
    current_datetime = datetime(2026, 5, 27, 4, 40)

    assert _can_run_now(current_datetime, (2,))


def test_can_run_now_before_window_is_blocked():
    current_datetime = datetime(2026, 5, 27, 4, 39)

    assert not _can_run_now(current_datetime, (2,))


def test_can_run_now_after_window_is_blocked():
    current_datetime = datetime(2026, 5, 27, 8, 31)

    assert not _can_run_now(current_datetime, (2,))


def test_can_run_now_on_wrong_day_is_blocked():
    current_datetime = datetime(2026, 5, 27, 5, 0)

    assert not _can_run_now(current_datetime, (0,))


def test_wait_until_run_time_before_741_returns_target_time():
    current_datetime = datetime(2026, 5, 27, 6, 15)

    result = _wait_until_run_time(current_datetime)

    assert result == datetime(2026, 5, 27, 7, 41)


def test_wait_until_run_time_after_741_returns_none():
    current_datetime = datetime(2026, 5, 27, 7, 50)

    result = _wait_until_run_time(current_datetime)

    assert result is None