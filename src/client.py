import requests
from typing import Any, Dict

from src.models import Stop
from src.exceptions import (
    ReservaDuplicadaError,
    FechaPasadaError,
    ReservaDesconocidaError,
)


class FonobusClient:
    BASE_URL = "https://fonobus.n1servers.com.ar"

    def __init__(self, token: str):
        self.headers = {
            "authorization": f"Bearer {token}",
            "content-type": "application/json",
            "accept": "application/json",
        }
        self.url = f"{self.BASE_URL}/api/v2/reserva"

    def _service_ids_from_stop(self, stop: Stop) -> list[int]:
        """Devuelve los services en orden de prioridad.
        Args:
            stop (Stop): La parada para la cual se desean obtener los service IDs.
        Returns:
            list[int]: Una lista de service IDs correspondientes a la parada especificada, ordenados por prioridad.
        Raises:
            ValueError: Si la parada no es reconocida.
        """
        if stop == Stop.PADUA:
            return [
                6097,  # 07:40 default
                4600,  # 07:30
                5284,  # 07:50
            ]

        if stop == Stop.CORRIENTES:
            return [
                4606,  # 16:20 default
                7411,  # 16:35
            ]
        raise ValueError(f"Parada desconocida: {stop}")

    def _create_single_reserva(
        self, stop_id: Stop, date: str, service_id: int
    ) -> Dict[str, Any]:
        payload = {
            "idService": service_id,
            "idStop": stop_id.value,
            "date": date,
        }

        response = requests.post(
            self.url,
            json=payload,
            headers=self.headers,
        )

        data: Dict[str, Any] = response.json()

        # ERRORES
        if data.get("status") == 400:
            error_msg: str = data.get("error", "")
            # fecha inválida → aborta
            if "anteriores al día y hora actuales" in error_msg:
                raise FechaPasadaError(error_msg)
            # ya reservada → aborta
            if "Ya posee una reserva" in error_msg:
                raise ReservaDuplicadaError(error_msg)
            if (
                "disponible" in error_msg.lower()
                or "no hay lugares" in error_msg.lower()
            ):
                raise ReservaDuplicadaError(error_msg)
            raise ReservaDesconocidaError(error_msg)

        if data.get("status") == 200:
            data["selected_service_id"] = service_id

        return data

    def create_reserva(self, stop_id: Stop, date: str) -> Dict[str, Any]:
        last_error = None

        for service_id in self._service_ids_from_stop(stop_id):
            print(f"Intentando reserva {stop_id} | service = {service_id}")

            try:
                data: Dict[str, Any] = self._create_single_reserva(
                    stop_id, date, service_id
                )
                # SUCCESS
                if data.get("status") == 200:
                    data["selected_service_id"] = service_id
                    return data
            except Exception as e:
                last_error = str(e)

        # ERRORES
        # fecha inválida → aborta
        if "anteriores al día y hora actuales" in last_error:
            raise FechaPasadaError(last_error)
        # ya reservada → aborta
        if "Ya posee una reserva" in last_error:
            raise ReservaDuplicadaError(last_error)
        if (
            "disponible" in last_error.lower()
            or "no hay lugares" in last_error.lower()
        ):
            raise ReservaDuplicadaError(last_error)
        raise ReservaDesconocidaError(last_error)
