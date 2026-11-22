# Pruebas unitarias para la jerarquia de excepciones de Software FJ
import unittest
from software_fj.excepciones import (
    SoftwareFJError,
    ValidacionError,
    ClienteInvalidoError,
    ParametroFaltanteError,
    ServicioInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    CalculoInconsistenteError,
    EntidadNoEncontradaError
)

class TestExcepcionesSoftwareFJ(unittest.TestCase):
    # Verifica que todas las excepciones del dominio hereden de la clase base SoftwareFJError
    def test_herencia_base(self):
        excepciones = [
            ValidacionError,
            ClienteInvalidoError,
            ParametroFaltanteError,
            ServicioInvalidoError,
            ServicioNoDisponibleError,
            ReservaInvalidaError,
            OperacionNoPermitidaError,
            CalculoInconsistenteError,
            EntidadNoEncontradaError
        ]
        for exc in excepciones:
            with self.subTest(excepcion=exc.__name__):
                self.assertTrue(issubclass(exc, SoftwareFJError))

    # Verifica que las excepciones de validacion compartan la clase padre ValidacionError
    def test_herencia_validacion(self):
        excepciones_validacion = [
            ClienteInvalidoError,
            ParametroFaltanteError,
            ServicioInvalidoError
        ]
        for exc in excepciones_validacion:
            with self.subTest(excepcion=exc.__name__):
                self.assertTrue(issubclass(exc, ValidacionError))

    # Verifica que el formato de cadena incluya el codigo entre corchetes
    def test_formato_codigo_mensaje(self):
        error = ClienteInvalidoError("Datos incompletos")
        self.assertEqual(error.codigo, "SFJ-101")
        self.assertEqual(str(error), "[SFJ-101] Datos incompletos")

    # Verifica la preservacion de la causa en el encadenamiento de excepciones
    def test_encadenamiento_de_excepciones(self):
        try:
            try:
                int("invalido")
            except ValueError as error_raiz:
                raise CalculoInconsistenteError("Fallo de conversion") from error_raiz
        except CalculoInconsistenteError as error_final:
            self.assertIsNotNone(error_final.__cause__)
            self.assertIsInstance(error_final.__cause__, ValueError)

if __name__ == "__main__":
    unittest.main()
