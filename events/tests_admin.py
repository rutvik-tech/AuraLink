from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Event
from django.utils import timezone


class AdminEventManagementTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.admin = User.objects.create_superuser('admin2', 'admin2@example.com', 'pass')
        self.user = User.objects.create_user('user1', 'u1@example.com', 'pass')
        self.event = Event.objects.create(
            title='ToDelete',
            description='x',
            start_time=timezone.now(),
            end_time=timezone.now(),
            venue='Place',
            price=0,
            capacity=10,
            organizer=self.admin
        )

    def test_admin_can_delete_event(self):
        self.client.login(username='admin2', password='pass')
        resp = self.client.post(reverse('delete_event', kwargs={'pk': self.event.pk}))
        self.assertRedirects(resp, reverse('dashboard'))
        self.assertFalse(Event.objects.filter(pk=self.event.pk).exists())

    def test_non_staff_cannot_delete(self):
        self.client.login(username='user1', password='pass')
        resp = self.client.post(reverse('delete_event', kwargs={'pk': self.event.pk}))
        self.assertEqual(resp.status_code, 403)
        self.assertTrue(Event.objects.filter(pk=self.event.pk).exists())

    def test_staff_quick_create_creates_event(self):
        from django.utils import timezone
        from datetime import timedelta
        self.staff = get_user_model().objects.create_user('staff1', 's1@example.com', 'pass')
        self.staff.is_staff = True
        self.staff.save()
        self.client.login(username='staff1', password='pass')
        start = (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')
        end = (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        resp = self.client.post(reverse('home'), {
            'create-event-submit': '1',
            'title': 'QuickEvent',
            'description': 'Quick desc',
            'start_time': start,
            'end_time': end,
            'venue': 'Hall',
            'price': '10.00',
            'capacity': '50',
        })
        # should redirect to dashboard on success
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Event.objects.filter(title='QuickEvent').exists())
