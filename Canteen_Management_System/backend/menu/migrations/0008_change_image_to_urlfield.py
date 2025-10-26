# Generated manually to fix image field

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_add_default_menu_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]