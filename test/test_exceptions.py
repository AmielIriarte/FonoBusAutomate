if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core import Stop
from src.client import FonobusClient
from src.config import config
from src.exceptions import (
    ReservaDuplicadaError,
    FechaPasadaError
)

def test_fecha_pasada():
    client = FonobusClient(config.FONOBUS_TOKEN)

    try:
        client.create_reserva(
            Stop.PADUA,
            "2020-01-01"
        )
    except FechaPasadaError:
        print("Fecha pasada detectada OK")


def test_reserva_duplicada():
    client = FonobusClient(config.FONOBUS_TOKEN)

    try:
        client.create_reserva(
            Stop.PADUA,
            "2026-05-23"
        )
    except ReservaDuplicadaError:
        print("Reserva duplicada detectada OK")
