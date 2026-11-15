from abc import ABC, abstractmethod
from software_fj.excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError
)
from software_fj.registro import obtener_logger

log = obtener_logger("modelos")

class EntidadBase(ABC):
    def __init__(self, id_entidad):
        self._id_entidad = id_entidad

    @property
    def id_entidad(self):
        return self._id_entidad

    @abstractmethod
    def get_detalles(self):
        pass


class Cliente(EntidadBase):
    def __init__(self, cedula, nombre, correo):
        super().__init__(cedula)
        if not cedula or not nombre or not correo:
            log.error("Faltan datos del cliente.")
            raise ParametroFaltanteError("Todos los campos son obligatorios.")
        if not str(cedula).isdigit():
            log.warning(f"Cédula inválida: {cedula}")
            raise ClienteInvalidoError("La cédula debe contener solo números.")
        
        self.__nombre = nombre
        self.__correo = correo
        log.info(f"Cliente registrado: {nombre}")

    @property
    def nombre(self):
        return self.__nombre

    @property
    def correo(self):
        return self.__correo

    def get_detalles(self):
        return f"Cliente: {self.__nombre} - CC: {self.id_entidad}"


class Servicio(EntidadBase, ABC):
    def __init__(self, codigo, nombre_serv, costo_base):
        super().__init__(codigo)
        if costo_base < 0:
            log.error("Costo base negativo.")
            raise CalculoInconsistenteError("El costo base no puede ser negativo.")
        self.nombre_serv = nombre_serv
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_detalles(self):
        pass


class SalaReunion(Servicio):
    def __init__(self, codigo, nombre, costo_base, capacidad):
        super().__init__(codigo, nombre, costo_base)
        if capacidad <= 0:
            raise CalculoInconsistenteError("Capacidad inválida.")
        self.capacidad = capacidad

    def calcular_costo(self, horas, descuento=0.0):
        if horas <= 0:
            log.warning("Horas inválidas para sala.")
            raise CalculoInconsistenteError("Las horas deben ser mayores a cero.")
        return (self.costo_base * horas) * (1.0 - descuento)

    def get_detalles(self):
        return f"Sala: {self.nombre_serv} (Cap: {self.capacidad})"


class AlquilerEquipo(Servicio):
    def __init__(self, codigo, nombre, costo_base, tipo):
        super().__init__(codigo, nombre, costo_base)
        self.tipo = tipo

    def calcular_costo(self, dias, seguro=False):
        if dias <= 0:
            log.warning("Días inválidos para equipo.")
            raise CalculoInconsistenteError("Los días deben ser mayores a cero.")
        total = self.costo_base * dias
        if seguro:
            total += 15000 * dias
        return total

    def get_detalles(self):
        return f"Equipo: {self.nombre_serv} tipo {self.tipo}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, nombre, costo_base, experto):
        super().__init__(codigo, nombre, costo_base)
        self.experto = experto

    def calcular_costo(self, sesiones, iva=0.19):
        if sesiones <= 0:
            log.warning("Sesiones inválidas para asesoría.")
            raise CalculoInconsistenteError("Las sesiones deben ser mayores a cero.")
        return (self.costo_base * sesiones) * (1.0 + iva)

    def get_detalles(self):
        return f"Asesoría: {self.nombre_serv} con {self.experto}"


class Reserva(EntidadBase):
    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        if not cliente or not servicio:
            log.error("Reserva sin cliente o servicio.")
            raise ReservaInvalidaError("Se requiere cliente y servicio válidos.")
        if duracion <= 0:
            log.error("Duración inválida.")
            raise ReservaInvalidaError("La duración debe ser positiva.")
        
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        log.info(f"Reserva creada: {id_reserva}")

    def confirmar(self):
        if self.estado == "Confirmada":
            raise OperacionNoPermitidaError("La reserva ya está confirmada.")
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("No se puede confirmar una reserva cancelada.")
        self.estado = "Confirmada"
        log.info(f"Reserva {self.id_entidad} confirmada.")

    def cancelar(self):
        if self.estado == "Cancelada":
            raise OperacionNoPermitidaError("La reserva ya fue cancelada antes.")
        self.estado = "Cancelada"
        log.warning(f"Reserva {self.id_entidad} cancelada.")

    def get_detalles(self):
        return f"Reserva {self.id_entidad} [{self.estado}] - {self.cliente.nombre} / {self.servicio.nombre_serv}"
