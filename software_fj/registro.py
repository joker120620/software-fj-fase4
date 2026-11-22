# Modulo de configuracion del sistema de logs para Software FJ
# Permite registrar eventos informativos, advertencias y excepciones en archivo

import logging
import os
from pathlib import Path

# Se define la ruta base del directorio de logs
DIRECTORIO_RAIZ = Path(__file__).resolve().parent.parent
CARPETA_LOGS = DIRECTORIO_RAIZ / "logs"
ARCHIVO_LOGS = CARPETA_LOGS / "software_fj.log"

def obtener_logger(nombre_modulo):
    # Se garantiza la creacion del directorio logs antes de escribir
    os.makedirs(CARPETA_LOGS, exist_ok=True)

    # Se obtiene la instancia de logger correspondiente al modulo
    logger = logging.getLogger(nombre_modulo)

    # Se agregan los manejadores solo si el logger no ha sido configurado previamente
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Formato unificado de cada linea de log
        formato = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # Manejador para almacenar los eventos en archivo de texto
        manejador_archivo = logging.FileHandler(str(ARCHIVO_LOGS), encoding="utf-8")
        manejador_archivo.setLevel(logging.DEBUG)
        manejador_archivo.setFormatter(formato)
        logger.addHandler(manejador_archivo)

        # Manejador para salida simultanea en consola
        manejador_consola = logging.StreamHandler()
        manejador_consola.setLevel(logging.INFO)
        manejador_consola.setFormatter(formato)
        logger.addHandler(manejador_consola)

    return logger
