if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import Stop
from src.client import FonobusClient
from src.config import config


def test_connection():
    client = FonobusClient(config.FONOBUS_TOKEN)

    response = client.create_reserva(
        stop_id=Stop.PADUA,
        date="2026-05-22"
    )
    print(response)
    assert "status" in response


if __name__ == "__main__":
    test_connection()
