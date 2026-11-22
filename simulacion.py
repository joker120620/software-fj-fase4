# Script principal de simulacion del sistema Software FJ
# Ejecuta operaciones completas para demostrar estabilidad, POO y manejo de excepciones

from software_fj.modelos import (
    Cliente,
    SalaReunion,
    AlquilerEquipo,
    AsesoriaEspecializada,
    Reserva,
    GestorReservas
)
from software_fj.excepciones import SoftwareFJError
from software_fj.registro import obtener_logger

# Se obtiene el logger para el script de simulacion
log = obtener_logger("simulacion")

def ejecutar_simulacion():
    # Mensaje inicial de inicio de la simulacion
    log.info("Iniciando bateria de simulacion del sistema Software FJ")
    print("=" * 70)
    print("SIMULACION INTEGRAL DEL SISTEMA SOFTWARE FJ - FASE 4")
    print("Manejo avanzado de excepciones y arquitectura orientada a objetos")
    print("=" * 70)

    # Se instancia el gestor con sus listas internas en memoria
    gestor = GestorReservas()

    # Definicion de casos de prueba simulados
    casos = [
        (
            "1. Registro exitoso de cliente en el gestor",
            lambda: gestor.registrar_cliente(Cliente("1098765432", "Carlos Rodriguez", "carlos@correo.com"))
        ),
        (
            "2. Intento de registro con cedula no numerica (encadenamiento)",
            lambda: Cliente("1098ABC", "Ana Perez", "ana@correo.com")
        ),
        (
            "3. Intento de registro con campos vacios (parametro faltante)",
            lambda: Cliente("", "Pedro Lopez", "pedro@correo.com")
        ),
        (
            "4. Creacion y registro exitoso de servicio Sala de Reuniones",
            lambda: gestor.registrar_servicio(SalaReunion("SR-101", "Sala Ejecutiva Principal", 45000, 12))
        ),
        (
            "5. Calculo incorrecto de horas en sala (calculo inconsistente)",
            lambda: gestor.buscar_servicio("SR-101").calcular_costo(0)
        ),
        (
            "6. Registro y calculo exitoso de Alquiler de Equipo con seguro",
            lambda: gestor.registrar_servicio(AlquilerEquipo("EQ-201", "Portatil para Desarrollo", 60000, "Computo"))
        ),
        (
            "7. Calculo sobrecargado de Alquiler con recargo de seguro por 3 dias",
            lambda: gestor.buscar_servicio("EQ-201").calcular_costo(3, seguro=True)
        ),
        (
            "8. Registro exitoso de Asesoria Especializada con calculo de IVA",
            lambda: gestor.registrar_servicio(AsesoriaEspecializada("AS-301", "Consultoria en Ciberseguridad", 120000, "Ing. Juan Toloza"))
        ),
        (
            "9. Busqueda en lista interna de cliente no existente",
            lambda: gestor.buscar_cliente("99999999")
        ),
        (
            "10. Creacion y confirmacion exitosa de una reserva",
            lambda: paso_reserva_exitosa(gestor)
        ),
        (
            "11. Procesamiento y liquidacion final de la reserva confirmada",
            lambda: paso_procesar_reserva(gestor)
        ),
        (
            "12. Intento de reserva con servicio inactivo o no disponible",
            lambda: paso_servicio_no_disponible(gestor)
        ),
        (
            "13. Intento de operacion no permitida (doble cancelacion de reserva)",
            lambda: paso_cancelacion_duplicada()
        )
    ]

    # Iteracion sobre cada operacion simulada demostrando continuidad ante fallos
    for numero, (descripcion, operacion) in enumerate(casos, 1):
        print(f"\n[Operacion {numero}] {descripcion}")
        try:
            # Se ejecuta la logica de la operacion
            resultado = operacion()
        except SoftwareFJError as err_controlado:
            # Captura de cualquier excepcion del dominio del sistema
            log.error(f"Excepcion controlada en op {numero} [{err_controlado.codigo}]: {err_controlado.mensaje}")
            print(f"  Resultado: Controlado -> [{err_controlado.codigo}] {err_controlado.mensaje}")
            # Si existio encadenamiento tecnico se muestra la causa raiz
            if err_controlado.__cause__:
                print(f"  Causa tecnica original: {type(err_controlado.__cause__).__name__} -> {err_controlado.__cause__}")
        except Exception as err_inesperado:
            # Captura de errores no previstos para evitar detencion abrupta
            log.critical(f"Error inesperado en op {numero}: {err_inesperado}")
            print(f"  Resultado: Error no previsto -> {err_inesperado}")
        else:
            # Se ejecuta cuando no se genero ninguna excepcion
            log.info(f"Operacion {numero} completada satisfactoriamente")
            if hasattr(resultado, "get_detalles"):
                print(f"  Resultado exitoso: {resultado.get_detalles()}")
            else:
                print(f"  Resultado exitoso: {resultado}")
        finally:
            # Bloque de cierre que siempre se ejecuta para cada ciclo
            print(f"  Ciclo de operacion {numero} finalizado.")

    print("\n" + "=" * 70)
    print("FIN DE LA SIMULACION - TODAS LAS OPERACIONES FUERON EJECUTADAS")
    print("Los eventos y errores han sido registrados en logs/software_fj.log")
    print("=" * 70)


def paso_reserva_exitosa(gestor):
    # Genera una reserva y confirma su estado
    res = gestor.crear_reserva("RES-001", "1098765432", "SR-101", 4)
    res.confirmar()
    return res


def paso_procesar_reserva(gestor):
    # Procesa la reserva existente RES-001 calculando el total con 10% de descuento
    reservas = gestor.listar_reservas()
    res = reservas[0]
    total = res.procesar(descuento=0.10)
    return f"Reserva {res.id_entidad} liquidada por un total de ${total}"


def paso_servicio_no_disponible(gestor):
    # Cambia la disponibilidad de un servicio para demostrar la excepcion
    serv = gestor.buscar_servicio("EQ-201")
    serv.disponible = False
    # Al intentar crear la reserva debe levantarse ServicioNoDisponibleError
    return gestor.crear_reserva("RES-002", "1098765432", "EQ-201", 2)


def paso_cancelacion_duplicada():
    # Instancia una reserva local y la cancela dos veces seguidas
    c = Cliente("11223344", "Marta Gómez", "marta@correo.com")
    s = SalaReunion("SR-999", "Sala Temporal", 30000, 6)
    r = Reserva("RES-LOCAL", c, s, 2)
    r.cancelar()
    # La segunda cancelacion debe generar OperacionNoPermitidaError
    r.cancelar()
    return r


if __name__ == "__main__":
    ejecutar_simulacion()
