from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import Config
from src.models import Weekdays, Stop
from src.client import FonobusClient
from src.core import run_reservation

day_schedule_mapping = {
    Weekdays.MONDAY: "tue",
    Weekdays.TUESDAY: "wed",
    Weekdays.WEDNESDAY: "thu",
    Weekdays.THURSDAY: "fri",
    Weekdays.FRIDAY: "sat",
}


class Scheduler:
    """Clase encargada de programar la creación de reservas en días específicos de la semana.
    Utiliza APScheduler para manejar la programación de tareas y se encarga de ejecutar la función de reserva en los días indicados, manejando los posibles errores y enviando notificaciones por email.
    Args:
        client (FonobusClient): Instancia del cliente para interactuar con la API de Fonqbus.
        config (Config): Configuración con los parámetros necesarios para la reserva y el envío de emails.
    """

    def __init__(self, client: FonobusClient, config: Config):
        self._scheduler: BlockingScheduler = BlockingScheduler()
        self._client: FonobusClient = client
        self._config: Config = config

    def add_job(self, reserve_day: Weekdays, stop: Stop, exec_hour: int = 7, exec_minute: int = 10):
        """Agrega un job al scheduler para el día especificado a la hora indicada.

        Args:
            reserve_day (Weekdays): El día de la semana para el cual se desea programar la reserva.
            stop (Stop): La parada de la reserva (punto de encuentro).
            exec_hour (int): La hora del día (en formato 24h) para ejecutar el job.
            exec_minute (int): El minuto de la hora para ejecutar el job.
        """
        self._scheduler.add_job(
            lambda: run_reservation(reserve_day, stop, self._client, self._config),
            "cron",
            day_of_week=day_schedule_mapping[reserve_day],
            hour=exec_hour,
            minute=exec_minute,
        )

    def start(self):
        """Inicia el scheduler, bloqueando el hilo principal y ejecutando los jobs programados
        en los días y horas indicados."""
        self._scheduler.start()
