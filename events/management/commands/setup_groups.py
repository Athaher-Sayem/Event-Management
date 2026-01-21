from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from events.models import Event, Category
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates default groups (Admin, Organizer, Participant) with appropriate permissions'

    def handle(self, *args, **options):
        # Create Admin group
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admin group'))
        else:
            self.stdout.write(self.style.WARNING('Admin group already exists'))

        # Create Organizer group
        organizer_group, created = Group.objects.get_or_create(name='Organizer')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Organizer group'))
        else:
            self.stdout.write(self.style.WARNING('Organizer group already exists'))

        # Create Participant group
        participant_group, created = Group.objects.get_or_create(name='Participant')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Participant group'))
        else:
            self.stdout.write(self.style.WARNING('Participant group already exists'))

        # Get content types
        event_content_type = ContentType.objects.get_for_model(Event)
        category_content_type = ContentType.objects.get_for_model(Category)
        user_content_type = ContentType.objects.get_for_model(User)

        # Assign permissions to Organizer group
        organizer_permissions = [
            Permission.objects.get(codename='add_event', content_type=event_content_type),
            Permission.objects.get(codename='change_event', content_type=event_content_type),
            Permission.objects.get(codename='delete_event', content_type=event_content_type),
            Permission.objects.get(codename='view_event', content_type=event_content_type),
            Permission.objects.get(codename='add_category', content_type=category_content_type),
            Permission.objects.get(codename='change_category', content_type=category_content_type),
            Permission.objects.get(codename='delete_category', content_type=category_content_type),
            Permission.objects.get(codename='view_category', content_type=category_content_type),
        ]
        organizer_group.permissions.set(organizer_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned permissions to Organizer group'))

        # Assign permissions to Admin group (all permissions)
        admin_permissions = Permission.objects.all()
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned all permissions to Admin group'))

        # Participant group has view permissions only (default, no need to explicitly set)
        participant_permissions = [
            Permission.objects.get(codename='view_event', content_type=event_content_type),
            Permission.objects.get(codename='view_category', content_type=category_content_type),
        ]
        participant_group.permissions.set(participant_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned view permissions to Participant group'))

        self.stdout.write(self.style.SUCCESS('\nGroups setup completed successfully!'))
