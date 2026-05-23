if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.core import get_target_date, Weekdays


def test_tuesday_logic():
    result = get_target_date(Weekdays.MONDAY)
    print(result)
    assert result is not None


def test_thursday_logic():
    result = get_target_date(Weekdays.WEDNESDAY)
    print(result)
    assert result is not None


if __name__ == "__main__":
    test_tuesday_logic()
    test_thursday_logic()
