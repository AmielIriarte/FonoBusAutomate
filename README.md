# FonoBusAutomate

Automatización de reservas en Fonobus con notificaciones por email.

## ¿Qué hace este proyecto?

Este script crea reservas de combi automáticamente para días y paradas configuradas, con dos modos de ejecución:

- **Ejecución única**: corre una vez y termina.
- **Modo scheduler**: queda corriendo y ejecuta reservas en los horarios programados.

También envía emails para informar resultados y errores.

## Requisitos

- Python **3.12+**
- Token de Fonobus
- Credenciales SMTP (Gmail)

## Instalación

```bash
python -m pip install -e .
```

## Configuración

1. Copiá `.env.example` a `.env`
2. Completá las variables:

```env
FONOBUS_TOKEN=

EMAIL_FROM=
EMAIL_PASS=
EMAIL_TO=

RUN_SCHEDULER=0
```

### Variables de entorno

- `FONOBUS_TOKEN`: token Bearer para la API de Fonobus.
- `EMAIL_FROM`: cuenta Gmail origen.
- `EMAIL_PASS`: App Password de Gmail.
- `EMAIL_TO`: cuenta destino para notificaciones.
- `RUN_SCHEDULER`:
  - `0` → ejecución única.
  - `1` → modo continuo con scheduler.

## Uso

```bash
python main.py
```

## Configuración de reservas

En `main.py`, la función `reservation_config()` define qué reservas ejecutar:

- Lunes → `PADUA` y `CORRIENTES`
- Miércoles → `PADUA` y `CORRIENTES`

Podés modificar esa lista para agregar/quitar combinaciones día/parada.

## Estructura principal

- `main.py`: punto de entrada y selección de modo.
- `src/client.py`: cliente HTTP para crear reservas en Fonobus.
- `src/core.py`: lógica de fechas y ejecución de reservas.
- `src/scheduler.py`: programación con APScheduler.
- `src/emailer.py`: envío de notificaciones por SMTP.
- `src/lock.py`: evita ejecutar la misma reserva más de una vez por día.

## Tests

```bash
python -m pytest
```

> Nota: varios tests interactúan con servicios externos (API de Fonobus/SMTP), por lo que pueden fallar si no hay red, token válido o credenciales correctas.

## Dependencias

- `requests`
- `python-dotenv`
- `apscheduler`
- `pytest`
