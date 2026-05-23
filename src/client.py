import requests
from enum import StrEnum
from typing import Any, Dict

from src.exceptions import (
    ReservaDuplicadaError,
    FechaPasadaError,
    ReservaDesconocidaError,
)


class Stop(StrEnum):
    """Enum que representa las paradas disponibles para la reserva."""

    PADUA = "DIRECTORIO Y RIVADAVIA"
    CORRIENTES = "AV CORRIENTES 316"


def service_id_from_stop(stop: Stop) -> int:
    """Función que devuelve el ID del servicio correspondiente a una parada específica.
    Args:
        stop (Stop): La parada para la cual se desea obtener el ID del servicio.
    Returns:
        int: El ID del servicio correspondiente a la parada.
    Raises:
        ValueError: Si la parada no es reconocida.
    """
    if stop == Stop.PADUA:
        return 6097
    if stop == Stop.CORRIENTES:
        return 4606
    raise ValueError(f"Parada desconocida: {stop}")


class FonobusClient:
    BASE_URL = "https://fonobus.n1servers.com.ar"

    def __init__(self, token: str):
        self.headers = {
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "accept": "application/json",
        }

    def create_reserva(self, stop_id: Stop, date: str):
        url = f"{self.BASE_URL}/api/v2/reserva"
        service_id = service_id_from_stop(stop_id)
        payload = {"idService": service_id, "idStop": stop_id.value, "date": date}
        response = requests.post(url, json=payload, headers=self.headers)

        data: Dict[str, Any] = response.json()

        # MANEJO DE ERRORES
        if data.get("status") == 400:
            error_msg = data.get("error", "")
            if "anteriores al día y hora actuales" in error_msg:
                raise FechaPasadaError(error_msg)
            if "Ya posee una reserva" in error_msg:
                raise ReservaDuplicadaError(error_msg)
            raise ReservaDesconocidaError(error_msg)

        # SUCCESS
        if data.get("status") == 200:
            return data

        raise ReservaDesconocidaError(f"Respuesta inesperada: {data}")
