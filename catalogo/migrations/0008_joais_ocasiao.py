# Generated by Django 5.2.3 on 2025-07-11 02:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0007_populate_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='joais',
            name='ocasiao',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalogo.ocasiao'),
        ),
    ]
