class FonobusError(Exception):
    pass


class ReservaDuplicadaError(FonobusError):
    pass


class FechaPasadaError(FonobusError):
    pass


class ReservaDesconocidaError(FonobusError):
    pass
