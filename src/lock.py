from datetime import datetime
from pathlib import Path
from src.models import Stop, Weekdays

LOCK_DIR = Path(".locks")
LOCK_DIR.mkdir(exist_ok=True)


def _lock_name(day: Weekdays, stop: Stop) -> Path:
    today = datetime.now().strftime("%Y-%m-%d")
    return LOCK_DIR / f"{day}_{stop}_{today}.lock"


def already_executed(day: Weekdays, stop: Stop) -> bool:
    return _lock_name(day, stop).exists()


def mark_executed(day: Weekdays, stop: Stop) -> None:
    _lock_name(day, stop).touch()
