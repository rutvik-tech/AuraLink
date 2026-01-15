from django.core.management.base import BaseCommand
from events.models import Event
import random

class Command(BaseCommand):
    help = 'Updates event descriptions with varied, engaging text based on keywords.'

    def handle(self, *args, **kwargs):
        events = Event.objects.all()
        count = 0
        
        descriptions = {
            'music': (
                "Get ready for an unforgettable night of music and rhythm! "
                "Join us as top artists take the stage to perform their greatest hits. "
                "Experience the energy, the lights, and the sound in a venue designed for acoustics. "
                "Grab your tickets now and be part of the musical magic!"
            ),
            'tech': (
                "Dive into the future of technology at this exclusive event. "
                "Connect with industry leaders, developers, and innovators. "
                "Featuring keynote speeches, hands-on workshops, and demos of the latest gadgets. "
                "Whether you are a coding pro or a tech enthusiast, this is the place to be."
            ),
            'art': (
                "Immerse yourself in a world of creativity and expression. "
                "This exhibition showcases breathtaking works from renowned and emerging artists. "
                "Explore diverse mediums, attend artist talks, and find inspiration in every corner. "
                "A perfect outing for art lovers and creative souls."
            ),
            'business': (
                "Unlock new opportunities and expand your professional network. "
                "Join entrepreneurs, investors, and visionaries for a day of insightful discussions. "
                "Learn strategies for growth, leadership, and innovation in today's market. "
                "Elevate your career and business to the next level."
            ),
            'sports': (
                "Feel the adrenaline and the spirit of competition! "
                "Whether you are participating or cheering, the energy here is unmatched. "
                "Witness incredible feats of athleticism and sportsmanship. "
                "Bring your friends and family for a day of action and fun."
            ),
            'default': [
                "Join us for an exciting event featuring industry experts, interactive sessions, and great networking opportunities. Don't miss this chance to learn, connect, and grow!",
                "Experience an event like no other! We have curated a fantastic lineup of activities and speakers just for you. Reserve your spot today and make memories that will last a lifetime.",
                "Looking for something amazing to do? This event promises entertainment, education, and engagement. Perfect for individuals and groups alike. See you there!"
            ]
        }

        for event in events:
            title_lower = event.title.lower()
            
            if any(x in title_lower for x in ['music', 'concert', 'band', 'song', 'dj', 'fest']):
                desc = descriptions['music']
            elif any(x in title_lower for x in ['tech', 'code', 'hack', 'ai', 'soft', 'web', 'data']):
                desc = descriptions['tech']
            elif any(x in title_lower for x in ['art', 'design', 'paint', 'gallery', 'exhibit']):
                desc = descriptions['art']
            elif any(x in title_lower for x in ['business', 'startup', 'market', 'money', 'finance', 'lead']):
                desc = descriptions['business']
            elif any(x in title_lower for x in ['sport', 'run', 'yoga', 'fit', 'game', 'match']):
                desc = descriptions['sports']
            else:
                desc = random.choice(descriptions['default'])
            
            event.description = desc
            event.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} event descriptions with varied text.'))
