from django.db import migrations

def create_initial_data(apps, schema_editor):
    Categorias = apps.get_model('catalogo', 'Categorias')
    SubCategorias = apps.get_model('catalogo', 'SubCategorias')
    Material = apps.get_model('catalogo', 'Material')
    Ocasiao = apps.get_model('catalogo', 'Ocasiao')  # Note: removi o acento para evitar problemas

    # Categorias e Subcategorias melhor estruturadas
    categorias_subcategorias = {
        "Pulseiras": [
            "Pulseira de Prata",
            "Pulseira de Ouro",
            "Pulseira de Couro",
            "Pulseira com Pingentes",
            "Pulseira de Pedras",
            "Pulseira Infantil",
            "Pulseira Tennis"
        ],
        "Colares": [
            "Colar Delicado",
            "Colar Choker",
            "Colar Longo",
            "Colar com Pingente",
            "Colar de Pérolas",
            "Colar Infantil"
        ],
        "Anéis": [
            "Anel Solitário",
            "Aliança",
            "Anel de Noivado",
            "Anel com Pedras",
            "Anel Banhado a Ouro",
            "Anel de Formatura",
            "Anel Statement"
        ],
        "Brincos": [
            "Brincos de Argola",
            "Brincos de Pedra",
            "Brincos de Nascimento",
            "Brincos de Prata",
            "Brincos de Ouro",
            "Brincos Infantis",
            "Brincos de Diamante"
        ],
        "Conjuntos": [
            "Conjunto de Noiva",
            "Conjunto Banhado a Ouro",
            "Conjunto de Prata",
            "Conjunto Infantil",
            "Conjunto de Pérolas"
        ],
        "Pingentes": [
            "Pingente de Letra",
            "Pingente de Nome",
            "Pingente de Símbolo",
            "Pingente de Pedra",
        ]
    }

    
    for categoria, subcategorias in categorias_subcategorias.items():
        cat_obj, _ = Categorias.objects.get_or_create(nome=categoria)
        for subcategoria in subcategorias:
            SubCategorias.objects.get_or_create(nome=subcategoria, categoria=cat_obj)

    # Materiais (mantive seus originais e adicionei alguns)
    materiais = [
        "Prata 925",
        "Banhado a Ouro",
        "Ouro 18k",
        "Ouro Branco",
        "Ouro Rosé",
        "Aço Inoxidável",
        "Ouro 14k",
        "Platina",
        "Pérola",
        "Diamante",
        "Pedras Coloridas",
        "Couro Genuíno"
    ]

    for nome in materiais:
        Material.objects.get_or_create(material=nome)

    
    ocasioes = [
        "Namoro/Amor",
        "Noivado",
        "Casamento",
        "Formatura",
        "Presente Especial",
        "Uso Diário",
        "Eventos Formais"
    ]

    for nome in ocasioes:
        Ocasiao.objects.get_or_create(ocasiao=nome)

class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0006_categorias_alter_joais_options_subcategorias'),
    ]

    operations = [
        migrations.RunPython(create_initial_data),
    ]