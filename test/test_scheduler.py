if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scheduler import Scheduler
from src.config import Config
from src.core import Weekdays
from src.client import FonobusClient, Stop



if __name__ == "__main__":
    client = FonobusClient(Config.FONOBUS_TOKEN)
    scheduler = Scheduler(client, Config)

    dia = Weekdays.MONDAY
    parada = Stop.PADUA
    hora = 7
    minuto = 10

    scheduler.add_job(dia, parada, hora, minuto)

    scheduler.start()
