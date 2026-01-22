# import os
# import django
# import random
# from faker import Faker
# from django.utils import timezone # We need this to get "Right Now"

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
# django.setup()

# from events.models import Category, Event, Participant

# def populate_db():
#     fake = Faker()
#     print("Populating database...")

#     category_choices = [
#         ('SEM', 'Seminar'),
#         ('WRK', 'Workshop'),
#         ('SOC', 'Social Party'),
#         ('MEET', 'Official Meeting'),
#     ]
    
#     all_categories = []
#     for code, name in category_choices:
#         cat, created = Category.objects.get_or_create(
#             cat_name=code,
#             defaults={'cat_description': f"Description for {name} category."}
#         )
#         all_categories.append(cat)
    
#     print(f"Created/Loaded {len(all_categories)} categories.")

#     all_events = []
#     for _ in range(10):  # Let's create 10 events
        
#         # --- NEW CODE STARTS HERE ---
#         # 1. We pick a random type: Past, Present, or Future
#         time_type = random.choice(['past', 'present', 'future'])

#         if time_type == 'past':
#             # Pick a date from the last 30 days
#             my_date = fake.past_datetime(start_date='-30d', tzinfo=timezone.get_current_timezone())
        
#         elif time_type == 'future':
#             # Pick a date in the next 30 days
#             my_date = fake.future_datetime(end_date='+30d', tzinfo=timezone.get_current_timezone())
        
#         else:
#             # Pick exactly right now (Today)
#             my_date = timezone.now()
#         # --- NEW CODE ENDS HERE ---

#         event = Event.objects.create(
#             event_name=fake.catch_phrase(),
#             event_description=fake.text(),
#             location=fake.city(),
#             date_time=my_date, # We use the date we just picked
#             category=random.choice(all_categories)
#         )
#         all_events.append(event)
    
#     print(f"Created {len(all_events)} events with mixed dates.")

 
#     participants = []
#     for _ in range(20):  # Let's create 20 participants
#         parti = Participant.objects.create(
#             parti_name=fake.name(),
#             email=fake.unique.email()
#         )
        
#         events_to_assign = random.sample(all_events, k=random.randint(1, 4))
#         parti.events.set(events_to_assign)
        
#         participants.append(parti)

#     print(f"Created {len(participants)} participants and assigned events to them.")
#     print("Database populated successfully!")

# if __name__ == '__main__':
#     populate_db()

import os
import django
import random
from faker import Faker
from django.utils import timezone
from django.contrib.auth import get_user_model

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

User = get_user_model()

from events.models import Category, Event, RSPV

def populate_db():
    fake = Faker()
    print("Starting database population...\n")

    # ── 1. Categories ───────────────────────────────────────────────
    category_choices = [
        ('SEM', 'Seminar'),
        ('WRK', 'Workshop'),
        ('CON', 'Conference'),
        ('NET', 'Networking Event'),
        ('PAR', 'Party / Social'),
        ('OTH', 'Other'),
    ]

    categories = []
    for code, name in category_choices:
        cat, created = Category.objects.get_or_create(
            cat_name=code,
            defaults={'cat_description': f"All about {name.lower()} events."}
        )
        if created:
            print(f"Created category: {cat}")
        categories.append(cat)

    print(f"\n→ {len(categories)} categories ready\n")

    # ── 2. Create some realistic users ───────────────────────────────
    users = []
    User.objects.filter(username__startswith='fakeuser_').delete()  # clean previous fakes (optional)

    for i in range(18):
        username = f"fakeuser_{i+1}"
        email = f"fake{i+1}@example Events.test"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': email,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'password': 'pbkdf2_sha256$720000$abc$fakehashedpassword1234567890',  # dummy – never login with this
            }
        )
        if created:
            print(f"Created user: {user.username}")
        users.append(user)

    # Add one superuser-like account for testing (optional)
    admin, _ = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True,
            'password': 'pbkdf2_sha256$720000$xyz$fakeadminhashdontuseinprod',
        }
    )
    if admin not in users:
        users.append(admin)

    print(f"\n→ {len(users)} users ready (including admin)\n")

    # ── 3. Create events with varied dates (past / today / future) ───
    events = []

    for i in range(14):
        time_type = random.choice(['past', 'near_past', 'today', 'soon', 'future'])

        if time_type == 'past':
            dt = fake.past_datetime(start_date='-60d')
        elif time_type == 'near_past':
            dt = fake.past_datetime(start_date='-14d')
        elif time_type == 'today':
            dt = timezone.now() + random.choice([
                timezone.timedelta(hours=-3),
                timezone.timedelta(hours=2),
                timezone.timedelta(hours=5),
            ])
        elif time_type == 'soon':
            dt = timezone.now() + timezone.timedelta(days=random.randint(1, 9))
        else:
            dt = fake.future_datetime(end_date='+45d')

        # make sure it's aware
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)

        event = Event.objects.create(
            event_name       = fake.catch_phrase() + " " + fake.word().capitalize(),
            event_description= fake.paragraph(nb_sentences=random.randint(3,7)),
            location         = fake.city() + ", " + fake.country(),
            date_time        = dt,
            category         = random.choice(categories),
            image            = 'default_img.jpg',  # or leave blank if you have media setup
        )

        events.append(event)
        print(f"Created event: {event.event_name[:48]:<48}  {dt.strftime('%Y-%m-%d %H:%M')}")

    print(f"\n→ {len(events)} events created\n")

    # ── 4. Create realistic RSVPs ────────────────────────────────────
    rsvp_count = 0

    for event in events:
        # How many people are interested/going?
        possible_rsvp_users = random.sample(users, k=random.randint(2, len(users)-3))
        
        for user in possible_rsvp_users:
            # Sometimes skip (not everyone RSVPs)
            if random.random() < 0.35:
                continue
                
            RSPV.objects.get_or_create(
                event=event,
                user=user
            )
            rsvp_count += 1

    print(f"→ Created {rsvp_count} RSVP entries\n")

    print("Database population finished! ✓")
    print(f"Summary:")
    print(f"  • Categories : {Category.objects.count()}")
    print(f"  • Events     : {Event.objects.count()}")
    print(f"  • Users      : {User.objects.filter(username__startswith='fake').count()} fake + real ones")
    print(f"  • RSVPs      : {RSPV.objects.count()}\n")


if __name__ == '__main__':
    populate_db()