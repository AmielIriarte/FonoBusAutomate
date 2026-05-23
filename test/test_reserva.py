from datetime import datetime, timedelta

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core import Stop
from src.client import FonobusClient
from src.config import config


def test_create_reserva():
    client = FonobusClient(config.FONOBUS_TOKEN)
    today = datetime.now()
    next_week_day = (today + timedelta(days=6)).strftime("%Y-%m-%d")

    response = client.create_reserva(
        stop_id=Stop.PADUA, date=next_week_day
    )

    print("\nRESPONSE:")
    print(response)
    assert response["status"] == 200


if __name__ == "__main__":
    client = FonobusClient(config.FONOBUS_TOKEN)

    today = datetime.now()
    next_week_day = (today + timedelta(days=6)).strftime("%Y-%m-%d")
    next_week_day = "2026-05-26"  # Para pruebas fijas

    try:
        response = client.create_reserva(
            stop_id=Stop.CORRIENTES, date=next_week_day
        )
        print(response)
    except Exception as e:
        print(f"ERROR: {e}")
