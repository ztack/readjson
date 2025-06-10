import argostranslate.package
import argostranslate.translate

# Actualizar lista de paquetes disponibles
argostranslate.package.update_package_index()

# Buscar paquete EN → ES
available_packages = argostranslate.package.get_available_packages()
en_es_pkg = next(p for p in available_packages if p.from_code == "en" and p.to_code == "es")

# Instalar el paquete
path = en_es_pkg.download()
argostranslate.package.install_from_path(path)
