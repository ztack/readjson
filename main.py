import json
import logging
from argostranslate import translate

# Configurar logging a consola y archivo
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("ejecucion.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# Cargar archivo JSON
with open('exercises.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = len(data)
logging.info(f"Procesando TODOS los ejercicios (total: {total}).")

# Preparar traductor Argos (EN → ES)
installed_languages = translate.get_installed_languages()
from_lang = next((lang for lang in installed_languages if lang.code == "en"), None)
to_lang = next((lang for lang in installed_languages if lang.code == "es"), None)

if not from_lang or not to_lang:
    logging.error("Los idiomas en → es no están instalados. Ejecuta primero el instalador de paquetes.")
    exit(1)

translation = from_lang.get_translation(to_lang)

resultados = []

for idx, ejercicio in enumerate(data, start=1):
    logging.info(f"Ejercicio {idx}: {ejercicio['name']}")

    force_en            = ejercicio.get("force") or ""
    level_en            = ejercicio.get("level") or ""
    equipment_en        = ejercicio.get("equipment") or ""
    category_en         = ejercicio.get("category") or ""
    primary_en          = " ".join(ejercicio.get("primaryMuscles", []))
    secondary_en        = " ".join(ejercicio.get("secondaryMuscles", []))
    instrucciones_en    = " ".join(ejercicio.get("instructions", []))

    force_es            = translation.translate(force_en)
    level_es            = translation.translate(level_en)
    equipment_es        = translation.translate(equipment_en)
    category_es         = translation.translate(category_en)
    primary_es          = translation.translate(primary_en)
    secondary_es        = translation.translate(secondary_en)
    instrucciones_es    = translation.translate(instrucciones_en)

    
    nuevo = {
        "id": ejercicio["id"],
        "name": ejercicio["name"],
        "force": force_es,
        "level": level_es,
        "equipment": equipment_es,
        "primaryMuscles": primary_es,
        "secondaryMuscles": secondary_es,
        "instructions": [instrucciones_es],
        "category": category_es
    }
    resultados.append(nuevo)
    logging.info("✅ Traducido y agregado al resultado.")

    # Guardar archivo de salida
    salida_nombre = f"exercises_traducidos.json"
    with open(salida_nombre, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

logging.info(f"🎉 Archivo '{salida_nombre}' generado con éxito.")
