from django.db import migrations
from django.utils.text import slugify

def populate_categorias_slug(apps, schema_editor):
    Categorias = apps.get_model('catalogo', 'Categorias')
    for categoria in Categorias.objects.all():
        if not categoria.slug:
            base_slug = slugify(categoria.nome)
            slug = base_slug
            contador = 1
            while Categorias.objects.filter(slug=slug).exclude(pk=categoria.pk).exists():
                slug = f"{base_slug}-{contador}"
                contador += 1
            categoria.slug = slug
            categoria.save()

class Migration(migrations.Migration):
    dependencies = [
        ('catalogo', '0014_categorias_slug_joais_categoria'),
    ]
    operations = [
        migrations.RunPython(populate_categorias_slug),
    ] 