import os
import django
import random
from faker import Faker


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
        event = Event.objects.create(
            event_name=fake.catch_phrase(),
            event_description=fake.text(),
            location=fake.city(),
            date_time=fake.date_time_this_year(),
            # Assign a random category object
            category=random.choice(all_categories)
        )
        all_events.append(event)
    
    print(f"Created {len(all_events)} events.")

 
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