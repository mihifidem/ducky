
# abrir terminal y ejecutar python manage.py shell   python manage.py shell
# copiar el script en la shell y ejecutar
# salir de la shell con exit
# apareceran en la tabla languages los idiomas
# linea para hacer un commit.. ( ni caso)




from account.cv_manager.models import Language

# Lista de idiomas comunes
idiomas = [
    "Inglés",
    "Español",
    "Francés",
    "Alemán",
    "Italiano",
    "Portugués",
    "Chino",
    "Japonés",
    "Ruso",
    "Árabe"
]

# Crear los idiomas si no existen
for nombre in idiomas:
    Language.objects.get_or_create(name=nombre)

print("✅ Idiomas inicializados correctamente.")
