from enum import IntEnum
from datetime import datetime, timedelta

from src.config import Config
from src.client import FonobusClient, Stop
from src.emailer import send_email
from src.exceptions import (
    ReservaDuplicadaError,
    FechaPasadaError,
    ReservaDesconocidaError,
)


class Weekdays(IntEnum):
    """Enum que representa los días de la semana para la reserva."""
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4

    @staticmethod
    def get_values():
        """Función que devuelve una lista con los valores de los días de la semana definidos en el enum."""
        return [day.value for day in Weekdays]


def get_target_date(target_day: Weekdays):
    """Función que calcula la fecha del próximo día de la semana especificado.
    Args:
        target_day (Weekdays): El día de la semana para el cual se desea calcular la fecha.
    Returns:
        datetime: La fecha del próximo día de la semana especificado.
    Raises:
        ValueError: Si el día de la semana no es reconocido.
    """
    today = datetime.now()

    if target_day not in Weekdays.get_values():
        raise ValueError(
            f"Valor incorrecto para la variable día: {target_day}"
        )

    # días hasta próxima ocurrencia
    days_until = (
        target_day - today.weekday() + 7
    ) % 7

    # si da hoy o ya pasó -> próxima semana
    if days_until <= 0:
        days_until += 7

    target_date = today + timedelta(
        days=days_until
    )

    return target_date


def format_date(dt: datetime):
    """Función que formatea un objeto datetime a string en formato YYYY-MM-DD,
    requerido por la API de Fonobus.
    Args:
        dt (datetime): El objeto datetime a formatear.
    Returns:
        str: La fecha formateada como string en formato YYYY-MM-DD.
    """
    return dt.strftime("%Y-%m-%d")


def date_condition(day: Weekdays) -> bool:
    """Función que verifica si el día actual es el mismo que el día objetivo (más un día) para la reserva.
    Args:
        day (Weekdays): El día de la semana objetivo para la reserva.
    Returns:
        bool: True si el día actual es el mismo que el día objetivo más un día, False en caso contrario.
    """
    today = datetime.now()
    return today.weekday() == day + 1


def run_reservation(day: Weekdays, dest: Stop, client: FonobusClient, config: Config) -> None:
    """Ejecuta la creación de una reserva y notifica el resultado por email.

    Args:
        day (Weekdays): Día de la semana objetivo.
        dest (Stop): Parada destino.
        client (FonobusClient): Cliente de Fonobus.
        config (Config): Configuración de la aplicación.
    """
    try:
        if not date_condition(day):
            print(f"Omitiendo ciclo para día: {day} - parada: {dest}...")
            return

        print(f"Ejecutando job para día: {day} - parada: {dest}")
        target = get_target_date(day)
        date_str = format_date(target)

        response = client.create_reserva(dest, date_str)

        print(f"Reserva creada correctamente para día: {day} - parada: {dest}")
        send_email(
            "✔ Reserva OK - Fonobus",
            f"""
Reserva creada correctamente.

Fecha: {date_str}

Respuesta:
{response}
                """,
            config,
        )
    except ReservaDuplicadaError as e:
        print(f"Error: Reserva ya existente para {day} - {dest}")
        send_email("⚠ Reserva ya existente - Fonobus", str(e), config)
    except FechaPasadaError as e:
        print(f"Error: Fecha inválida para {day} - {dest}")
        send_email("⚠ Fecha inválida - Fonobus", str(e), config)
    except ReservaDesconocidaError as e:
        print(f"Error: Error desconocido para {day} - {dest}")
        send_email("❌ Error desconocido Fonobus", str(e), config)
    except Exception as e:
        print(f"Error: Error crítico para {day} - {dest}")
        send_email("🔥 Error crítico - Fonobus", str(e), config)
