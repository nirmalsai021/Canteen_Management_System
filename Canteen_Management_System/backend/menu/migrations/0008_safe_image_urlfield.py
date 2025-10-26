# Safe migration to change image field to URLField

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_add_default_menu_items'),
    ]

    operations = [
        # First, remove the old image field
        migrations.RemoveField(
            model_name='menuitem',
            name='image',
        ),
        # Then add the new URLField
        migrations.AddField(
            model_name='menuitem',
            name='image',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]