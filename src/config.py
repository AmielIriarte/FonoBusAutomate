import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Clase de configuración que carga los parámetros necesarios desde las variables de entorno.
    Atributos:
        FONOBUS_TOKEN (str): Token de autenticación para la API de Fonobus.
        EMAIL_FROM (str): Dirección de correo electrónico desde la cual se enviarán las notificaciones.
        EMAIL_PASS (str): Contraseña de la dirección de correo electrónico.
        EMAIL_TO (str): Dirección de correo electrónico a la cual se enviarán las notificaciones.
        RUN_SCHEDULER (bool): Indica si se debe ejecutar el programador de reservas.
    """
    FONOBUS_TOKEN = os.getenv("FONOBUS_TOKEN")

    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    EMAIL_TO = os.getenv("EMAIL_TO")

    RUN_SCHEDULER: bool = int(os.getenv("RUN_SCHEDULER", "0")) == 1


config = Config()
