from django.db import migrations

def create_initial_sectors(apps, schema_editor):
    Sector = apps.get_model('forum', 'Sector')
    sectores = [
        'Legal',
        'Salud',
        'Educación',
        'Finanzas',
        'Gestión',
        'Programación',
        'Marketing',
        'Otro'
    ]
    for nombre in sectores:
        Sector.objects.create(nombre=nombre)

class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0005_alter_respuesta_professional_answer'),
    ]

    operations = [
        migrations.RunPython(create_initial_sectors),
    ]