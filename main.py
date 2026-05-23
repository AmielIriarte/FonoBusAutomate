from src.config import config
from src.core import Weekdays, run_reservation
from src.client import FonobusClient, Stop
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


def run():
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
