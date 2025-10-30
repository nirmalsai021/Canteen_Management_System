from django.db import models
import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('drinks', 'Drinks'),
        ('snacks', 'Snacks'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    available = models.BooleanField(default=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='snacks')
    image = models.ImageField(upload_to='menu_images/', null=True, blank=True)

    def __str__(self):
        return self.name

@receiver(post_delete, sender=MenuItem)
def delete_image_file_on_delete(sender, instance, **kwargs):
    # Skip deletion for URL-based images (external URLs)
    if instance.image and hasattr(instance.image, 'path'):
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

@receiver(pre_save, sender=MenuItem)
def delete_old_image_on_update(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = MenuItem.objects.get(pk=instance.pk)
    except MenuItem.DoesNotExist:
        return
    old_image = old_instance.image
    new_image = instance.image
    # Skip deletion for URL-based images (external URLs)
    if old_image and old_image != new_image and hasattr(old_image, 'path'):
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)
