# Modulo de excepciones personalizadas para el sistema Software FJ
# Contiene la jerarquia de errores que permite controlar situaciones del dominio

class SoftwareFJError(Exception):
    # Excepcion base de la cual heredan todas las excepciones del sistema
    def __init__(self, mensaje, codigo="SFJ-000"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo

    def __str__(self):
        # Retorna el codigo de error junto al mensaje descriptivo
        return f"[{self.codigo}] {self.mensaje}"


class ValidacionError(SoftwareFJError):
    # Error base para inconsistencias o fallos en la validacion de datos
    def __init__(self, mensaje, codigo="SFJ-100"):
        super().__init__(mensaje, codigo)


class ClienteInvalidoError(ValidacionError):
    # Se genera cuando los datos del cliente no cumplen las restricciones definidas
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-101")


class ParametroFaltanteError(ValidacionError):
    # Se genera cuando faltan argumentos requeridos para completar una operacion
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-102")


class ServicioInvalidoError(ValidacionError):
    # Se genera ante parametros invalidos al construir un servicio
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-103")


class ServicioNoDisponibleError(SoftwareFJError):
    # Se genera cuando un servicio no se encuentra activo o disponible para reserva
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-200")


class ReservaInvalidaError(SoftwareFJError):
    # Se genera cuando la estructura o datos de la reserva son incorrectos
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-300")


class OperacionNoPermitidaError(SoftwareFJError):
    # Se genera al intentar transiciones de estado invalidas en las reservas
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-301")


class CalculoInconsistenteError(SoftwareFJError):
    # Se genera cuando un calculo aritmetico o de tarifa no es valido
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-400")


class EntidadNoEncontradaError(SoftwareFJError):
    # Se genera al buscar una entidad (cliente o servicio) inexistente en las listas
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-500")
