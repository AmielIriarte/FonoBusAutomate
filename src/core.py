from enum import IntEnum, StrEnum
from datetime import datetime, timedelta


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
