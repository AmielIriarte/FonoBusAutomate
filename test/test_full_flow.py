if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models import Weekdays, Stop
from src.client import FonobusClient
from src.core import get_target_date, format_date
from src.config import config
from src.emailer import send_email


def test_full_flow():
    client = FonobusClient(config.FONOBUS_TOKEN)

    target = get_target_date(Weekdays.MONDAY)
    date_str = format_date(target)

    response = client.create_reserva(
        stop_id=Stop.PADUA,
        date=date_str
    )

    print(response)

    send_email(
        subject="TEST FULL FLOW",
        body=str(response),
        config=config
    )

    assert response["status"] == 200
