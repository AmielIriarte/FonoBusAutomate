import os
from dotenv import load_dotenv

load_dotenv()


def _parse_run_days(raw_value: str | None) -> tuple[int, ...]:
    if not raw_value:
        return ()

    run_days = []
    for raw_day in raw_value.split(","):
        day = raw_day.strip()
        if not day:
            continue

        day_index = int(day)
        if day_index < 0 or day_index > 6:
            raise ValueError("RUN_DAYS debe contener valores entre 0 y 6")

        run_days.append(day_index)

    return tuple(run_days)


class Config:
    """Clase de configuración que carga los parámetros necesarios desde las variables de entorno.
    Atributos:
        FONOBUS_TOKEN (str): Token de autenticación para la API de Fonobus.
        EMAIL_FROM (str): Dirección de correo electrónico desde la cual se enviarán las notificaciones.
        EMAIL_PASS (str): Contraseña de la dirección de correo electrónico.
        EMAIL_TO (str): Dirección de correo electrónico a la cual se enviarán las notificaciones.
        RUN_SCHEDULER (bool): Indica si se debe ejecutar el programador de reservas.
        RUN_DAYS (tuple[int, ...]): Días habilitados para ejecutar la corrida manual.
    """
    FONOBUS_TOKEN = os.getenv("FONOBUS_TOKEN")

    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")

    RUN_SCHEDULER: bool = str(os.getenv("RUN_SCHEDULER", "0")) == "1"
    RUN_DAYS: tuple[int, ...] = _parse_run_days(os.getenv("RUN_DAYS"))


config = Config()
