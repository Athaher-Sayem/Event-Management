import os
import django
import random
from faker import Faker
from django.utils import timezone # We need this to get "Right Now"

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant

def populate_db():
    fake = Faker()
    print("Populating database...")

    category_choices = [
        ('SEM', 'Seminar'),
        ('WRK', 'Workshop'),
        ('SOC', 'Social Party'),
        ('MEET', 'Official Meeting'),
    ]
    
    all_categories = []
    for code, name in category_choices:
        cat, created = Category.objects.get_or_create(
            cat_name=code,
            defaults={'cat_description': f"Description for {name} category."}
        )
        all_categories.append(cat)
    
    print(f"Created/Loaded {len(all_categories)} categories.")

    all_events = []
    for _ in range(10):  # Let's create 10 events
        
        # --- NEW CODE STARTS HERE ---
        # 1. We pick a random type: Past, Present, or Future
        time_type = random.choice(['past', 'present', 'future'])

        if time_type == 'past':
            # Pick a date from the last 30 days
            my_date = fake.past_datetime(start_date='-30d', tzinfo=timezone.get_current_timezone())
        
        elif time_type == 'future':
            # Pick a date in the next 30 days
            my_date = fake.future_datetime(end_date='+30d', tzinfo=timezone.get_current_timezone())
        
        else:
            # Pick exactly right now (Today)
            my_date = timezone.now()
        # --- NEW CODE ENDS HERE ---

        event = Event.objects.create(
            event_name=fake.catch_phrase(),
            event_description=fake.text(),
            location=fake.city(),
            date_time=my_date, # We use the date we just picked
            category=random.choice(all_categories)
        )
        all_events.append(event)
    
    print(f"Created {len(all_events)} events with mixed dates.")

 
    participants = []
    for _ in range(20):  # Let's create 20 participants
        parti = Participant.objects.create(
            parti_name=fake.name(),
            email=fake.unique.email()
        )
        
        events_to_assign = random.sample(all_events, k=random.randint(1, 4))
        parti.events.set(events_to_assign)
        
        participants.append(parti)

    print(f"Created {len(participants)} participants and assigned events to them.")
    print("Database populated successfully!")

if __name__ == '__main__':
    populate_db()