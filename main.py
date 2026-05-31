from datetime import datetime, time
from time import sleep

from src.models import Stop
from src.config import config
from src.core import Weekdays, run_reservation
from src.client import FonobusClient
from src.scheduler import Scheduler


def reservation_config():
    return [
        (Weekdays.MONDAY, Stop.PADUA),
        (Weekdays.WEDNESDAY, Stop.PADUA),
        (Weekdays.MONDAY, Stop.CORRIENTES),
        (Weekdays.WEDNESDAY, Stop.CORRIENTES),
    ]


def run_continuos():
    client = FonobusClient(config.FONOBUS_TOKEN)
    scheduler: Scheduler = Scheduler(client, config)

    print("Scheduler iniciado correctamente. Configurando jobs...")
    for day, stop in reservation_config():
        scheduler.add_job(day, stop)

    print("Iniciando scheduler...")
    scheduler.start()


def _is_within_run_window(current_time: time) -> bool:
    return time(4, 40) <= current_time <= time(8, 30)


def _can_run_now(current_datetime: datetime, allowed_days: tuple[int, ...]) -> bool:
    if allowed_days and current_datetime.weekday() not in allowed_days:
        return False

    return _is_within_run_window(current_datetime.time())


def _wait_until_run_time(current_datetime: datetime) -> datetime | None:
    target_datetime = current_datetime.replace(hour=7, minute=41, second=0, microsecond=0)

    if time(4, 40) <= current_datetime.time() < target_datetime.time():
        return target_datetime

    return None


def run():
    current_datetime = datetime.now()

    if not _can_run_now(current_datetime, config.RUN_DAYS):
        print("Fuera del día habilitado o de la ventana 04:40-08:30. No se ejecuta nada.")
        return

    wait_until = _wait_until_run_time(current_datetime)
    if wait_until is not None:
        seconds_to_wait = (wait_until - current_datetime).total_seconds()
        print("Esperando hasta las 07:41 para iniciar la ejecución...")
        sleep(seconds_to_wait)

    client = FonobusClient(config.FONOBUS_TOKEN)

    for day, stop in reservation_config():
        run_reservation(day, stop, client, config)


def main():
    if config.RUN_SCHEDULER:
        print("RUN_SCHEDULER está habilitado. Iniciando en modo continuo...")
        run_continuos()
    else:
        print("RUN_SCHEDULER está deshabilitado. Ejecutando una sola vez...")
        run()


if __name__ == "__main__":
    main()
