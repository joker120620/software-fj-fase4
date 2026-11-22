# Software FJ - Sistema Integral de Gestion de Clientes, Servicios y Reservas

Proyecto desarrollado para la **Fase 4 - Componente practico: Practicas simuladas** del curso **Programacion (213023)**, Escuela de Ciencias Basicas, Tecnologia e Ingenieria (ECBTI), UNAD.

## Informacion del Estudiante
- **Estudiante:** Juan David Toloza Ortega
- **Usuario GitHub:** [@joker120620](https://github.com/joker120620)
- **Grupo:** 213023_190
- **Tutor:** Jhon Harold Patiño Pantoja
- **Modalidad:** Desarrollo individual (asumido ante ausencia de comunicacion y coordinacion en el foro colaborativo)

## Descripcion del Sistema
Aplicacion orientada a objetos en Python desarrollada bajo principios de modularidad, encapsulacion, herencia, polimorfismo y manejo robusto de excepciones. El sistema gestiona clientes, servicios especializados (salas de reunion, alquiler de equipos y asesorias especializadas) y reservas, operando sin motores de base de datos relacionales mediante estructuras de objetos y listas en memoria, registrando las operaciones y excepciones en un archivo de logs.

## Requisitos de Ejecucion
- Python 3.10 o superior.
- Sin dependencias externas (utiliza unicamente la biblioteca estandar de Python).

## Estructura del Proyecto
```
software-fj-fase4/
├── logs/
│   └── software_fj.log       # Registro cronologico de eventos, errores y excepciones
├── software_fj/
│   ├── __init__.py           # Paquete principal
│   ├── excepciones.py        # Jerarquia de excepciones personalizadas con codigos SFJ
│   ├── modelos.py            # Entidades POO, servicios polimorficos, reservas y gestor
│   └── registro.py           # Configuracion del sistema centralizado de logs
├── tests/
│   ├── test_excepciones.py   # Pruebas unitarias de excepciones y encadenamiento
│   └── test_modelos.py       # Pruebas unitarias de modelos, reservas y gestor
├── simulacion.py             # Script de simulacion con 13 operaciones completas
└── README.md
```

## Jerarquia de Excepciones Personalizadas
Todas las excepciones del dominio heredan de la clase base `SoftwareFJError` y poseen un codigo identificador para trazabilidad en logs:

- `SoftwareFJError` (SFJ-000)
  - `ValidacionError` (SFJ-100)
    - `ClienteInvalidoError` (SFJ-101)
    - `ParametroFaltanteError` (SFJ-102)
    - `ServicioInvalidoError` (SFJ-103)
  - `ServicioNoDisponibleError` (SFJ-200)
  - `ReservaInvalidaError` (SFJ-300)
  - `OperacionNoPermitidaError` (SFJ-301)
  - `CalculoInconsistenteError` (SFJ-400)
  - `EntidadNoEncontradaError` (SFJ-500)

## Ejecucion de Pruebas Unitarias
Para ejecutar la suite completa de pruebas unitarias desde la raiz del proyecto:
```bash
python -m unittest discover -s tests -v
```

## Ejecucion de la Simulacion
Para ejecutar las operaciones simuladas y verificar el manejo de excepciones y generacion de logs:
```bash
python simulacion.py
```
