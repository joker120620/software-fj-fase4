class SoftwareFJError(Exception):
    def __init__(self, mensaje, codigo="SFJ-000"):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.codigo = codigo
    def __str__(self):
        return f"[{self.codigo}] {self.mensaje}"

class ValidacionError(SoftwareFJError):
    def __init__(self, mensaje, codigo="SFJ-100"):
        super().__init__(mensaje, codigo)

class ClienteInvalidoError(ValidacionError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-101")

class ParametroFaltanteError(ValidacionError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-102")

class ServicioInvalidoError(ValidacionError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-103")

class ServicioNoDisponibleError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-200")

class ReservaInvalidaError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-300")

class OperacionNoPermitidaError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-301")

class CalculoInconsistenteError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-400")

class EntidadNoEncontradaError(SoftwareFJError):
    def __init__(self, mensaje):
        super().__init__(mensaje, "SFJ-500")
