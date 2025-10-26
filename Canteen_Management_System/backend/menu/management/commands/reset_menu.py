from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Reset menu items with proper images'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Resetting menu items...')
        call_command('create_default_items')
        self.stdout.write('✅ Menu reset complete!')