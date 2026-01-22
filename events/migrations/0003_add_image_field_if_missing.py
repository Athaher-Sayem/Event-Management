# Generated manually to fix missing image column issue
# This migration adds the image column if it doesn't exist in the database
# This can happen if the database was created before the image field was added to the model

from django.db import migrations, models


def add_image_field_if_missing(apps, schema_editor):
    """
    Add image field to Event model if it doesn't exist in the database.
    Uses Django's schema editor to ensure proper field type.
    """
    Event = apps.get_model('events', 'Event')
    db_table = Event._meta.db_table
    
    with schema_editor.connection.cursor() as cursor:
        # Check if column exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT 1 FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = %s 
                AND column_name = 'image'
            );
        """, [db_table])
        column_exists = cursor.fetchone()[0]
        
        if not column_exists:
            # Use Django's schema editor to add the field properly
            field = models.ImageField(default='default_img.jpg', upload_to='event_images/')
            field.set_attributes_from_name('image')
            schema_editor.add_field(Event, field)


def remove_image_field_if_exists(apps, schema_editor):
    """Reverse migration - remove the field if it was added by this migration."""
    Event = apps.get_model('events', 'Event')
    try:
        field = Event._meta.get_field('image')
        schema_editor.remove_field(Event, field)
    except:
        # Field doesn't exist, nothing to remove
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_event_image'),
    ]

    operations = [
        migrations.RunPython(
            add_image_field_if_missing,
            reverse_code=remove_image_field_if_exists,
        ),
    ]
