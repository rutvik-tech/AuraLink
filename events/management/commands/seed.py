from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from events.models import Event, Registration, Category


class Command(BaseCommand):
    help = 'Seed the database with sample categories, events, an organizer and registrations'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create an organizer user
        organizer, created = User.objects.get_or_create(
            username='organizer',
            defaults={'email': 'organizer@example.com', 'is_staff': True, 'is_superuser': True}
        )
        if created:
            organizer.set_password('organizerpass')
            organizer.is_superuser = True
            organizer.is_staff = True
            organizer.save()
            self.stdout.write(self.style.SUCCESS('Created organizer (username=organizer, password=organizerpass)'))
        else:
            # ensure the user has necessary privileges
            if not organizer.is_superuser or not organizer.is_staff:
                organizer.is_superuser = True
                organizer.is_staff = True
                organizer.save()
            self.stdout.write(self.style.WARNING('Organizer user already exists (privileges ensured)'))

        now = timezone.now()

        # Define categories
        categories = {
            'Annual Plan': ['Annual College Event Plan (Full Year)'],
            'Academic & Technical Events': [
                'Orientation Program (First Year Students)',
                'Expert Lecture Series (Monthly)',
                'Technical Workshops (Embedded Systems, VLSI, AI, Web Dev)',
                'Coding Competition / Hackathon',
                'Project Exhibition',
                'Research Paper Presentation',
                'Industrial Visit',
                'Internship & Training Awareness Session'
            ],
            'Skill Development & Career Events': [
                'Resume Building Workshop',
                'Aptitude & Placement Training',
                'Mock Interviews & GD Sessions',
                'Higher Studies & GATE Awareness Program',
                'Entrepreneurship & Startup Talk',
                'Alumni Interaction Session'
            ],
            'Cultural Events': [
                "Fresher’s Party",
                'Traditional Day',
                'Cultural Fest (Dance, Music, Drama)',
                'Annual Day',
                'Talent Hunt',
                'Fashion Show',
                'Farewell Party'
            ],
            'Sports & Fitness Events': [
                'Sports Day',
                'Cricket / Football / Volleyball Tournament',
                'Indoor Games Competition (Chess, Carrom)',
                'Yoga & Meditation Session',
                'Fitness Challenge Week'
            ],
            'Social & Awareness Activities': [
                'Independence Day Celebration',
                'Republic Day Celebration',
                'Teachers’ Day Celebration',
                "Women’s Day Program",
                'Environmental Awareness Drive',
                'Tree Plantation Drive',
                'Blood Donation Camp',
                'Swachh Bharat Abhiyan',
                'NSS / Social Service Camp'
            ],
            'Club & Departmental Activities': [
                'Club Inauguration Ceremony',
                'Weekly Club Activities',
                'Department Day Celebration',
                'Technical Quiz',
                'Poster Presentation Competition',
                'Debate & Elocution Competition'
            ],
            'End-of-Year Events': [
                'Annual Prize Distribution',
                'Feedback & Review Meeting',
                'Student Achievement Recognition',
                'Planning Meeting for Next Academic Year'
            ]
        }

        # Create categories
        cat_objs = {}
        for cat_name in categories.keys():
            c, created = Category.objects.get_or_create(name=cat_name)
            cat_objs[cat_name] = c
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat_name}'))

        # Create events per category with unique slug handling
        from django.utils.text import slugify
        offset = 3
        for cat_name, events in categories.items():
            for i, title in enumerate(events):
                start = now + timedelta(days=offset + i * 7)
                end = start + timedelta(hours=3)
                defaults = {
                    'description': title,
                    'start_time': start,
                    'end_time': end,
                    'venue': 'Main Campus Auditorium',
                    'price': 0.00,
                    'capacity': 200,
                    'organizer': organizer,
                    'category': cat_objs[cat_name]
                }
                # Try to find by title first
                try:
                    ev = Event.objects.get(title=title)
                    created = False
                except Event.DoesNotExist:
                    # create with a unique slug
                    base_slug = slugify(title)[:200]
                    slug = base_slug
                    counter = 1
                    while Event.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    defaults['slug'] = slug
                    ev = Event.objects.create(title=title, **defaults)
                    created = True

                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created event: {ev.title} (Category: {cat_name})'))
                else:
                    # Ensure category is set
                    updated = False
                    if ev.category is None:
                        ev.category = cat_objs[cat_name]
                        updated = True
                    if ev.organizer is None:
                        ev.organizer = organizer
                        updated = True
                    if updated:
                        ev.save()
                        self.stdout.write(self.style.SUCCESS(f'Updated event for: {ev.title}'))
        self.stdout.write(self.style.SUCCESS('Seeding complete.'))
