from enum import IntEnum, StrEnum


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
