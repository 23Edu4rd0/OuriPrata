from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '0009_auto_20250711_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='material',
            old_name='material',
            new_name='nome',
        ),
        migrations.RenameField(
            model_name='ocasiao',
            old_name='ocasiao',
            new_name='nome',
        ),
    ]
