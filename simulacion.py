from software_fj.modelos import Cliente, SalaReunion, AlquilerEquipo, AsesoriaEspecializada, Reserva
from software_fj.excepciones import SoftwareFJError
from software_fj.registro import obtener_logger

log = obtener_logger("simulacion")

def ejecutar_simulacion():
    log.info("Iniciando pruebas del sistema")
    print("=" * 60)
    print(" PRUEBAS DEL SISTEMA SOFTWARE FJ ")
    print("=" * 60)
    
    operaciones = [
        lambda: Cliente("1098765432", "Carlos", "carlos@mail.com"),
        lambda: Cliente("abc", "Ana", "ana@mail.com"),
        lambda: SalaReunion("S1", "Principal", 50000, 10),
        lambda: SalaReunion("S2", "Secundaria", 40000, 5).calcular_costo(0),
        lambda: AlquilerEquipo("E1", "Laptop", 70000, "PC"),
        lambda: AlquilerEquipo("E1", "Laptop", 70000, "PC").calcular_costo(3, True),
        lambda: AsesoriaEspecializada("A1", "Redes", 100000, "Ing. Juan"),
        lambda: Reserva("R1", None, SalaReunion("S3", "Sala 3", 30000, 4), 2),
        lambda: flujo_ok(),
        lambda: flujo_error()
    ]

    for i, op in enumerate(operaciones, 1):
        print(f"\nEjecutando operacion {i}...")
        try:
            res = op()
        except SoftwareFJError as err:
            log.error(f"Error controlado [{err.codigo}]: {err}")
            print(f"  Excepción controlada: [{err.codigo}] {err}")
        except Exception as e:
            log.critical(f"Error inesperado: {e}")
            print(f"  Error crítico: {e}")
        else:
            log.info(f"Operación {i} completada sin novedad")
            print(f"  Éxito en op {i}: {res if res is not True else 'Completado'}")
        finally:
            print(f"  [finally] Cierre de ciclo {i}")

    print("\n" + "=" * 60)
    print("Simulación terminada.")
    print("=" * 60)

def flujo_ok():
    c = Cliente("11223344", "Luisa", "luisa@mail.com")
    s = SalaReunion("S99", "VIP", 60000, 8)
    r = Reserva("RES-10", c, s, 3)
    r.confirmar()
    return r.get_detalles()

def flujo_error():
    c = Cliente("99887766", "Pedro", "pedro@mail.com")
    s = AlquilerEquipo("E99", "Proyector", 30000, "Video")
    r = Reserva("RES-11", c, s, 1)
    r.cancelar()
    r.cancelar()
    return r

if __name__ == "__main__":
    ejecutar_simulacion()
