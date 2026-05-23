from apscheduler.schedulers.blocking import BlockingScheduler

from src.config import Config
from src.core import Weekdays, Stop, get_target_date, format_date
from src.client import FonobusClient
from src.emailer import send_email
from src.exceptions import (
    ReservaDuplicadaError,
    FechaPasadaError,
    ReservaDesconocidaError,
)

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

    def _run(self, day: Weekdays, dest: Stop):
        """Función que se ejecuta cada vez que se dispara el job programado.
        Se encarga de crear la reserva y manejar los posibles errores, enviando un email con el resultado.
        Args:
            day (Weekdays): El día de la semana para el cual se está intentando crear la reserva.
            dest (Stop): El destino de la reserva.
        """
        try:
            print(f"Ejecutando job para {day} - {dest}")
            target = get_target_date(day)
            date_str = format_date(target)

            response = self._client.create_reserva(
                dest, date_str
            )

            print(f"Reserva creada correctamente para {day} - {dest}")
            send_email(
                "✔ Reserva OK - Fonobus",
                f"""
Reserva creada correctamente.

Fecha: {date_str}

Respuesta:
{response}
                """,
                self._config,
            )
        except ReservaDuplicadaError as e:
            print(f"Error: Reserva ya existente para {day} - {dest}")
            send_email("⚠ Reserva ya existente - Fonobus", str(e), self._config)
        except FechaPasadaError as e:
            print(f"Error: Fecha inválida para {day} - {dest}")
            send_email("⚠ Fecha inválida - Fonobus", str(e), self._config)
        except ReservaDesconocidaError as e:
            print(f"Error: Error desconocido para {day} - {dest}")
            send_email("❌ Error desconocido Fonobus", str(e), self._config)
        except Exception as e:
            print(f"Error: Error crítico para {day} - {dest}")
            send_email("🔥 Error crítico - Fonobus", str(e), self._config)

    def add_job(self, reserve_day: Weekdays, stop: Stop, exec_hour: int = 0, exec_minute: int = 51):
        """Agrega un job al scheduler para el día especificado a la hora indicada.

        Args:
            reserve_day (Weekdays): El día de la semana para el cual se desea programar la reserva.
            stop (Stop): La parada de la reserva (punto de encuentro).
            exec_hour (int): La hora del día (en formato 24h) para ejecutar el job.
            exec_minute (int): El minuto de la hora para ejecutar el job.
        """
        self._scheduler.add_job(
            lambda: self._run(reserve_day, stop),
            "cron",
            day_of_week=day_schedule_mapping[reserve_day],
            hour=exec_hour,
            minute=exec_minute,
        )

    def start(self):
        """Inicia el scheduler, bloqueando el hilo principal y ejecutando los jobs programados
        en los días y horas indicados."""
        self._scheduler.start()
