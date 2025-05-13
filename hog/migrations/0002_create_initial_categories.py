from django.db import migrations

def create_categories(apps, schema_editor):
    EventCategory = apps.get_model('hog', 'EventCategory')
    EventCategory.objects.bulk_create([
        EventCategory(name='Queen Esther'),
        EventCategory(name='G.R.A.C.E')
    ])

class Migration(migrations.Migration):
    dependencies = [
        ('hog', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]