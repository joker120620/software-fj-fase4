# Modulo de modelos orientados a objetos para Software FJ
# Define entidades base, clases derivadas, encapsulacion, servicios, reservas y gestor interno

from abc import ABC, abstractmethod
from software_fj.excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
    EntidadNoEncontradaError
)
from software_fj.registro import obtener_logger

# Se obtiene el logger para el modulo de modelos
log = obtener_logger("modelos")


class EntidadBase(ABC):
    # Clase abstracta base que representa cualquier entidad identificable del sistema
    def __init__(self, id_entidad):
        # Atributo protegido que identifica de forma unica la entidad
        self._id_entidad = str(id_entidad).strip()

    @property
    def id_entidad(self):
        # Permite la consulta de solo lectura del identificador
        return self._id_entidad

    @abstractmethod
    def get_detalles(self):
        # Metodo polimorfico abstracto para obtener descripcion textual
        pass


class Cliente(EntidadBase):
    # Representa a un cliente con datos personales estrictamente encapsulados
    def __init__(self, cedula, nombre, correo):
        # Se verifica que ningun parametro sea nulo o vacio
        if not cedula or not nombre or not correo:
            log.error("Intento de creacion de cliente con campos obligatorios vacios.")
            raise ParametroFaltanteError("Todos los datos del cliente son obligatorios.")

        # Se inicializa el identificador en la clase padre
        super().__init__(cedula)

        # Se valida que la cedula contenga unicamente digitos numericos usando encadenamiento
        try:
            int(str(cedula).strip())
        except (ValueError, TypeError) as error:
            log.warning(f"Formato de cedula no numerico: {cedula}")
            # Encadenamiento de excepcion para conservar la causa tecnica original
            raise ClienteInvalidoError("La cedula debe contener unicamente digitos numericos.") from error

        # Se valida la estructura basica del correo electronico
        if "@" not in str(correo) or "." not in str(correo):
            log.warning(f"Formato de correo electronico incorrecto: {correo}")
            raise ClienteInvalidoError("El formato del correo electronico no es valido.")

        # Atributos privados para cumplir con encapsulacion estricta
        self.__nombre = str(nombre).strip()
        self.__correo = str(correo).strip()
        log.info(f"Cliente registrado satisfactoriamente: {self.__nombre} (CC: {self.id_entidad})")

    @property
    def nombre(self):
        # Acceso de solo lectura al nombre privado
        return self.__nombre

    @property
    def correo(self):
        # Acceso de solo lectura al correo privado
        return self.__correo

    def get_detalles(self):
        # Retorna el resumen del cliente para reportes y visualizacion
        return f"Cliente: {self.__nombre} | CC: {self.id_entidad} | Correo: {self.__correo}"


class Servicio(EntidadBase, ABC):
    # Clase abstracta que define la interfaz comun para todos los servicios de la empresa
    def __init__(self, codigo, nombre_serv, costo_base):
        # Se inicializa el codigo en la entidad base
        super().__init__(codigo)

        # Se valida que el nombre del servicio no este vacio
        if not nombre_serv or not str(nombre_serv).strip():
            log.error("Se intento crear un servicio con nombre vacio.")
            raise ParametroFaltanteError("El nombre del servicio es obligatorio.")

        # Se valida que el costo base sea numerico y no negativo mediante encadenamiento
        try:
            costo_numerico = float(costo_base)
        except (ValueError, TypeError) as error:
            log.error(f"Costo base no numerico: {costo_base}")
            raise CalculoInconsistenteError("El costo base debe ser un valor numerico.") from error

        if costo_numerico < 0:
            log.error(f"Costo base con valor negativo: {costo_numerico}")
            raise CalculoInconsistenteError("El costo base del servicio no puede ser negativo.")

        # Atributos comunes de servicio
        self.nombre_serv = str(nombre_serv).strip()
        self.costo_base = costo_numerico
        # Estado de disponibilidad del servicio
        self.disponible = True

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        # Metodo abstracto polimorfico y sobrecargado segun la logica del servicio
        pass

    @abstractmethod
    def get_detalles(self):
        # Metodo abstracto para la descripcion del servicio
        pass


class SalaReunion(Servicio):
    # Servicio especializado en alquiler de salas de conferencia
    def __init__(self, codigo, nombre, costo_base, capacidad):
        super().__init__(codigo, nombre, costo_base)

        # Se valida la capacidad de la sala mediante encadenamiento
        try:
            cap_entero = int(capacidad)
        except (ValueError, TypeError) as error:
            raise ServicioInvalidoError("La capacidad de la sala debe ser un numero entero.") from error

        if cap_entero <= 0:
            log.error(f"Capacidad de sala invalida: {cap_entero}")
            raise CalculoInconsistenteError("La capacidad de la sala debe ser mayor a cero.")

        self.capacidad = cap_entero

    def calcular_costo(self, horas, descuento=0.0):
        # Permite calcular la tarifa aplicando opcionalmente un porcentaje de descuento
        try:
            horas_num = float(horas)
            descuento_num = float(descuento)
        except (ValueError, TypeError) as error:
            log.error("Parametros no numericos en calculo de tarifa de sala.")
            raise CalculoInconsistenteError("Las horas y el descuento deben ser valores numericos.") from error

        if horas_num <= 0:
            log.warning("Calculo rechazado por cantidad de horas menor o igual a cero.")
            raise CalculoInconsistenteError("La cantidad de horas debe ser estrictamente mayor a cero.")

        if not (0.0 <= descuento_num < 1.0):
            log.warning(f"Descuento fuera de rango valido: {descuento_num}")
            raise CalculoInconsistenteError("El descuento debe estar entre 0.0 y menor a 1.0.")

        # Calculo con factor de descuento
        total = (self.costo_base * horas_num) * (1.0 - descuento_num)
        return round(total, 2)

    def get_detalles(self):
        estado_disp = "Disponible" if self.disponible else "No Disponible"
        return f"Sala: {self.nombre_serv} | Capacidad: {self.capacidad} personas | Tarifa base: ${self.costo_base}/h | Estado: {estado_disp}"


class AlquilerEquipo(Servicio):
    # Servicio especializado en alquiler de equipamiento tecnologico
    def __init__(self, codigo, nombre, costo_base, tipo):
        super().__init__(codigo, nombre, costo_base)
        if not tipo or not str(tipo).strip():
            raise ParametroFaltanteError("El tipo de equipo es obligatorio.")
        self.tipo = str(tipo).strip()

    def calcular_costo(self, dias, seguro=False):
        # Permite calcular el costo por dias con opcion de seguro adicional
        try:
            dias_num = int(dias)
        except (ValueError, TypeError) as error:
            log.error("Dias de alquiler con formato no numerico.")
            raise CalculoInconsistenteError("La cantidad de dias de alquiler debe ser un numero entero.") from error

        if dias_num <= 0:
            log.warning("Cantidad de dias de alquiler no valida.")
            raise CalculoInconsistenteError("Los dias de alquiler deben ser mayores a cero.")

        # Tarifa base acumulada por dia
        total = self.costo_base * dias_num
        # Si se solicita seguro, se suma recargo fijo diario de 15000
        if seguro:
            total += 15000 * dias_num
        return round(float(total), 2)

    def get_detalles(self):
        estado_disp = "Disponible" if self.disponible else "No Disponible"
        return f"Equipo: {self.nombre_serv} | Tipo: {self.tipo} | Tarifa base: ${self.costo_base}/dia | Estado: {estado_disp}"


class AsesoriaEspecializada(Servicio):
    # Servicio de asesoria y consultoria tecnica
    def __init__(self, codigo, nombre, costo_base, experto):
        super().__init__(codigo, nombre, costo_base)
        if not experto or not str(experto).strip():
            raise ParametroFaltanteError("El nombre del experto asesor es obligatorio.")
        self.experto = str(experto).strip()

    def calcular_costo(self, sesiones, iva=0.19):
        # Permite calcular el costo multiplicando sesiones y aplicando la tasa de impuesto
        try:
            sesiones_num = int(sesiones)
            iva_num = float(iva)
        except (ValueError, TypeError) as error:
            log.error("Parametros incorrectos en calculo de asesoria.")
            raise CalculoInconsistenteError("Las sesiones y el IVA deben ser valores numericos.") from error

        if sesiones_num <= 0:
            log.warning("Cantidad de sesiones no valida.")
            raise CalculoInconsistenteError("Las sesiones deben ser mayores a cero.")

        if iva_num < 0:
            log.warning("Valor de IVA negativo detectado.")
            raise CalculoInconsistenteError("El porcentaje de IVA no puede ser negativo.")

        total = (self.costo_base * sesiones_num) * (1.0 + iva_num)
        return round(float(total), 2)

    def get_detalles(self):
        estado_disp = "Disponible" if self.disponible else "No Disponible"
        return f"Asesoria: {self.nombre_serv} | Especialista: {self.experto} | Tarifa por sesion: ${self.costo_base} | Estado: {estado_disp}"


class Reserva(EntidadBase):
    # Representa la reserva de un servicio por parte de un cliente con gestion de estados
    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)

        # Se valida que el cliente y el servicio no sean nulos
        if cliente is None or servicio is None:
            log.error("Intento de creacion de reserva sin cliente o servicio asignado.")
            raise ReservaInvalidaError("Se requiere un cliente y un servicio validos para crear la reserva.")

        # Se valida la duracion mediante encadenamiento
        try:
            duracion_valida = float(duracion)
        except (ValueError, TypeError) as error:
            log.error(f"Duracion invalida en reserva {id_reserva}: {duracion}")
            raise ReservaInvalidaError("La duracion de la reserva debe ser un valor numerico.") from error

        if duracion_valida <= 0:
            log.error(f"Duracion menor o igual a cero en reserva {id_reserva}.")
            raise ReservaInvalidaError("La duracion de la reserva debe ser estrictamente positiva.")

        # Atributos principales de la reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion_valida
        self.estado = "Pendiente"
        self.costo_total = None
        log.info(f"Reserva creada: ID {self.id_entidad} - Cliente: {self.cliente.nombre} - Servicio: {self.servicio.nombre_serv}")

    def confirmar(self):
        # Cambia el estado a Confirmada tras verificar condiciones
        if self.estado == "Confirmada":
            log.warning(f"Intento de re-confirmar reserva {self.id_entidad}.")
            raise OperacionNoPermitidaError("La reserva ya se encuentra confirmada.")
        if self.estado == "Cancelada":
            log.warning(f"Intento de confirmar reserva previamente cancelada {self.id_entidad}.")
            raise OperacionNoPermitidaError("No se puede confirmar una reserva que ha sido cancelada.")
        if self.estado == "Procesada":
            log.warning(f"Intento de confirmar una reserva ya procesada {self.id_entidad}.")
            raise OperacionNoPermitidaError("La reserva ya fue procesada y finalizada.")

        self.estado = "Confirmada"
        log.info(f"Reserva {self.id_entidad} confirmada exitosamente.")
        return True

    def cancelar(self):
        # Permite cancelar una reserva activa
        if self.estado == "Cancelada":
            log.warning(f"Intento de cancelar una reserva ya cancelada {self.id_entidad}.")
            raise OperacionNoPermitidaError("La reserva ya fue cancelada previamente.")
        if self.estado == "Procesada":
            log.warning(f"Intento de cancelar una reserva que ya fue procesada {self.id_entidad}.")
            raise OperacionNoPermitidaError("No es posible cancelar una reserva que ya fue procesada.")

        self.estado = "Cancelada"
        log.warning(f"Reserva {self.id_entidad} marcada como cancelada.")
        return True

    def procesar(self, **kwargs):
        # Liquida la reserva, calcula el costo total y finaliza el ciclo
        if self.estado == "Cancelada":
            log.error(f"Fallo al procesar: la reserva {self.id_entidad} esta cancelada.")
            raise OperacionNoPermitidaError("No se puede procesar una reserva que se encuentra cancelada.")
        if self.estado == "Pendiente":
            log.error(f"Fallo al procesar: la reserva {self.id_entidad} no ha sido confirmada.")
            raise OperacionNoPermitidaError("La reserva debe confirmarse antes de proceder con el procesamiento.")

        # Se valida la disponibilidad del servicio
        if not self.servicio.disponible:
            log.error(f"El servicio {self.servicio.nombre_serv} no esta disponible para procesar la reserva.")
            raise ServicioNoDisponibleError(f"El servicio '{self.servicio.nombre_serv}' no se encuentra disponible.")

        # Se calcula el costo total utilizando el metodo polimorfico del servicio
        self.costo_total = self.servicio.calcular_costo(self.duracion, **kwargs)
        self.estado = "Procesada"
        log.info(f"Reserva {self.id_entidad} procesada con exito. Total liquidado: ${self.costo_total}")
        return self.costo_total

    def get_detalles(self):
        total_str = f" | Total: ${self.costo_total}" if self.costo_total is not None else ""
        return f"Reserva [{self.id_entidad}] | Estado: {self.estado} | Cliente: {self.cliente.nombre} | Servicio: {self.servicio.nombre_serv} | Duracion: {self.duracion}{total_str}"


class GestorReservas:
    # Administra las listas internas en memoria del sistema para clientes, servicios y reservas
    # Cumple el requisito de operar sin bases de datos relacionales
    def __init__(self):
        # Listas internas para el almacenamiento de objetos
        self._clientes = []
        self._servicios = []
        self._reservas = []
        log.info("Inicializado el gestor interno de Software FJ.")

    def registrar_cliente(self, cliente):
        # Agrega un cliente validado a la lista interna
        if not isinstance(cliente, Cliente):
            raise ClienteInvalidoError("El objeto a registrar debe ser una instancia valida de Cliente.")
        # Se verifica que no exista un cliente con la misma cedula
        for c in self._clientes:
            if c.id_entidad == cliente.id_entidad:
                raise ClienteInvalidoError(f"Ya existe un cliente registrado con la cedula {cliente.id_entidad}.")
        self._clientes.append(cliente)
        log.info(f"Cliente con cedula {cliente.id_entidad} agregado a la lista interna.")
        return cliente

    def registrar_servicio(self, servicio):
        # Agrega un servicio a la lista interna
        if not isinstance(servicio, Servicio):
            raise ServicioInvalidoError("El objeto debe ser una instancia valida de Servicio.")
        # Se verifica que el codigo de servicio no este duplicado
        for s in self._servicios:
            if s.id_entidad == servicio.id_entidad:
                raise ServicioInvalidoError(f"Ya existe un servicio registrado con el codigo {servicio.id_entidad}.")
        self._servicios.append(servicio)
        log.info(f"Servicio [{servicio.id_entidad}] registrado en el gestor.")
        return servicio

    def buscar_cliente(self, cedula):
        # Busca un cliente por su identificador en la lista interna
        cedula_str = str(cedula).strip()
        for cliente in self._clientes:
            if cliente.id_entidad == cedula_str:
                return cliente
        # Si no se encuentra se dispara la excepcion de entidad no encontrada
        log.error(f"Busqueda fallida: cliente con cedula {cedula_str} no encontrado.")
        raise EntidadNoEncontradaError(f"No se encontro ningun cliente con cedula {cedula_str}.")

    def buscar_servicio(self, codigo):
        # Busca un servicio por su codigo en la lista interna
        codigo_str = str(codigo).strip()
        for servicio in self._servicios:
            if servicio.id_entidad == codigo_str:
                return servicio
        log.error(f"Busqueda fallida: servicio con codigo {codigo_str} no encontrado.")
        raise EntidadNoEncontradaError(f"No se encontro ningun servicio con codigo {codigo_str}.")

    def crear_reserva(self, id_reserva, cedula_cliente, codigo_servicio, duracion):
        # Construye y almacena una reserva vinculando cliente y servicio existentes
        cliente = self.buscar_cliente(cedula_cliente)
        servicio = self.buscar_servicio(codigo_servicio)

        # Se comprueba la disponibilidad actual del servicio
        if not servicio.disponible:
            log.warning(f"Intento de reserva para servicio no disponible: {servicio.nombre_serv}")
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre_serv}' no esta disponible para nuevas reservas.")

        nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion)
        self._reservas.append(nueva_reserva)
        return nueva_reserva

    def listar_clientes(self):
        # Devuelve copia de la lista de clientes registrados
        return list(self._clientes)

    def listar_servicios(self):
        # Devuelve copia de la lista de servicios registrados
        return list(self._servicios)

    def listar_reservas(self):
        # Devuelve copia de la lista de reservas realizadas
        return list(self._reservas)
