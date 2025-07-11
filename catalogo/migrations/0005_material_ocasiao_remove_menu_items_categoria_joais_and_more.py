# Generated by Django 5.2.3 on 2025-07-10 18:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0004_alter_menu_items_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Ocasiao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocasiao', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='menu_items',
            name='categoria',
        ),
        migrations.CreateModel(
            name='Joais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='catalogo')),
                ('destaque', models.BooleanField(default=False)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogo.material')),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
            },
        ),
        migrations.DeleteModel(
            name='Categories',
        ),
        migrations.DeleteModel(
            name='Menu_Items',
        ),
    ]
