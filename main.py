from src.config import config
from src.core import Weekdays, Stop
from src.client import FonobusClient
from src.scheduler import Scheduler


def reservation_config():
    return [
        (Weekdays.MONDAY, Stop.PADUA),
        (Weekdays.WEDNESDAY, Stop.PADUA),
        (Weekdays.MONDAY, Stop.CORRIENTES),
        (Weekdays.WEDNESDAY, Stop.CORRIENTES),
    ]


def main():
    client = FonobusClient(config.FONOBUS_TOKEN)
    scheduler: Scheduler = Scheduler(client, config)

    print("Scheduler iniciado correctamente. Configurando jobs...")
    for day, stop in reservation_config():
        scheduler.add_job(day, stop)

    print("Iniciando scheduler...")
    scheduler.start()


if __name__ == "__main__":
    main()
