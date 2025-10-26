# Generated manually to add default menu items

from django.db import migrations

def create_default_menu_items(apps, schema_editor):
    # Skip creating items here - will be done after URLField migration
    pass

def reverse_default_menu_items(apps, schema_editor):
    MenuItem = apps.get_model('menu', 'MenuItem')
    MenuItem.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_alter_menuitem_category'),
    ]

    operations = [
        migrations.RunPython(create_default_menu_items, reverse_default_menu_items),
    ]