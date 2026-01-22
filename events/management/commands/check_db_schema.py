from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Checks if the database schema matches the models'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Check if events_event table exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'events_event'
                );
            """)
            table_exists = cursor.fetchone()[0]
            
            if not table_exists:
                self.stdout.write(self.style.ERROR('events_event table does not exist!'))
                self.stdout.write(self.style.WARNING('Run: python manage.py migrate'))
                return
            
            # Check if image column exists
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_schema = 'public' 
                    AND table_name = 'events_event' 
                    AND column_name = 'image'
                );
            """)
            image_exists = cursor.fetchone()[0]
            
            if not image_exists:
                self.stdout.write(self.style.ERROR('image column does not exist in events_event table!'))
                self.stdout.write(self.style.WARNING('Run: python manage.py migrate'))
                self.stdout.write(self.style.WARNING('This will apply pending migrations and add the missing column.'))
            else:
                self.stdout.write(self.style.SUCCESS('Database schema is correct. image column exists.'))
