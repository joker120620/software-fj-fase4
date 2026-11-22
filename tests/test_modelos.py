# Pruebas unitarias para los modelos, validaciones y gestor interno de Software FJ
import unittest
from software_fj.modelos import (
    Cliente,
    SalaReunion,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva,
    GestorReservas
)
from software_fj.excepciones import (
    ClienteInvalidoError,
    ParametroFaltanteError,
    CalculoInconsistenteError,
    ReservaInvalidaError,
    OperacionNoPermitidaError,
    ServicioNoDisponibleError,
    EntidadNoEncontradaError
)

class TestModelosSoftwareFJ(unittest.TestCase):
    def setUp(self):
        # Configuracion comun para cada caso de prueba
        self.gestor = GestorReservas()
        self.cliente = Cliente("100200300", "Laura Morales", "laura@correo.com")
        self.sala = SalaReunion("SR-01", "Sala de Juntas", 50000, 10)
        self.equipo = AlquilerEquipo("EQ-01", "Videoproyector HD", 40000, "Audiovisual")
        self.asesoria = AsesoriaEspecializada("AS-01", "Consultoria Contable", 80000, "Dra. Gomez")

    # Validaciones sobre la clase Cliente
    def test_cliente_valido_y_encapsulacion(self):
        self.assertEqual(self.cliente.id_entidad, "100200300")
        self.assertEqual(self.cliente.nombre, "Laura Morales")
        self.assertEqual(self.cliente.correo, "laura@correo.com")
        self.assertIn("100200300", self.cliente.get_detalles())

    def test_cliente_cedula_invalida(self):
        # Cédula no numérica debe disparar ClienteInvalidoError con causa
        with self.assertRaises(ClienteInvalidoError):
            Cliente("100ABC", "Laura Morales", "laura@correo.com")

    def test_cliente_parametros_faltantes(self):
        with self.assertRaises(ParametroFaltanteError):
            Cliente("", "Laura", "laura@correo.com")

    # Pruebas de polimorfismo y sobrecarga en calculo de costos
    def test_calculo_sala_con_descuento(self):
        # 50000 * 3 horas = 150000 con 20% descuento = 120000
        costo = self.sala.calcular_costo(3, descuento=0.20)
        self.assertEqual(costo, 120000.0)

    def test_calculo_sala_horas_invalidas(self):
        with self.assertRaises(CalculoInconsistenteError):
            self.sala.calcular_costo(0)

    def test_calculo_equipo_con_seguro(self):
        # 40000 * 2 dias = 80000 + (15000 * 2) = 110000
        costo = self.equipo.calcular_costo(2, seguro=True)
        self.assertEqual(costo, 110000.0)

    def test_calculo_asesoria_con_iva(self):
        # 80000 * 2 sesiones = 160000 * 1.19 = 190400
        costo = self.asesoria.calcular_costo(2, iva=0.19)
        self.assertEqual(costo, 190400.0)

    # Pruebas sobre la clase Reserva y sus estados
    def test_ciclo_de_vida_reserva_exitoso(self):
        reserva = Reserva("RES-T1", self.cliente, self.sala, 2)
        self.assertEqual(reserva.estado, "Pendiente")

        reserva.confirmar()
        self.assertEqual(reserva.estado, "Confirmada")

        total = reserva.procesar()
        self.assertEqual(reserva.estado, "Procesada")
        self.assertEqual(total, 100000.0)

    def test_reserva_cancelacion_duplicada(self):
        reserva = Reserva("RES-T2", self.cliente, self.equipo, 1)
        reserva.cancelar()
        self.assertEqual(reserva.estado, "Cancelada")
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.cancelar()

    def test_reserva_procesar_sin_confirmar(self):
        reserva = Reserva("RES-T3", self.cliente, self.asesoria, 1)
        with self.assertRaises(OperacionNoPermitidaError):
            reserva.procesar()

    def test_reserva_servicio_no_disponible(self):
        self.sala.disponible = False
        reserva = Reserva("RES-T4", self.cliente, self.sala, 2)
        reserva.confirmar()
        with self.assertRaises(ServicioNoDisponibleError):
            reserva.procesar()

    # Pruebas sobre el Gestor y listas internas
    def test_gestor_registro_y_busqueda(self):
        self.gestor.registrar_cliente(self.cliente)
        self.gestor.registrar_servicio(self.sala)

        encontrado_c = self.gestor.buscar_cliente("100200300")
        self.assertEqual(encontrado_c.nombre, "Laura Morales")

        encontrado_s = self.gestor.buscar_servicio("SR-01")
        self.assertEqual(encontrado_s.nombre_serv, "Sala de Juntas")

    def test_gestor_entidad_no_encontrada(self):
        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.buscar_cliente("999999")

        with self.assertRaises(EntidadNoEncontradaError):
            self.gestor.buscar_servicio("NO-EXISTE")

    def test_gestor_crear_reserva_servicio_no_disponible(self):
        self.gestor.registrar_cliente(self.cliente)
        self.equipo.disponible = False
        self.gestor.registrar_servicio(self.equipo)

        with self.assertRaises(ServicioNoDisponibleError):
            self.gestor.crear_reserva("RES-T5", "100200300", "EQ-01", 3)

if __name__ == "__main__":
    unittest.main()
