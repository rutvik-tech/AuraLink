from django.test import TestCase
from django.urls import reverse
from .models import Event, Registration
from django.utils import timezone


class RegistrationFlowTests(TestCase):
    def setUp(self):
        self.event = Event.objects.create(
            title='Test Event',
            description='Desc',
            start_time=timezone.now(),
            end_time=timezone.now(),
            venue='Nowhere',
            price=0.00,
            capacity=10,
        )

    def test_free_registration_creates_registration_and_sends_email(self):
        resp = self.client.post(reverse('event_detail', kwargs={'slug': self.event.slug}), {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone': '123'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Registration.objects.count(), 1)

    def test_paid_checkout_creates_registration_and_redirects(self):
        self.event.price = 20
        self.event.save()
        resp = self.client.post(reverse('checkout', kwargs={'slug': self.event.slug}), {
            'full_name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '555'
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Registration.objects.count(), 1)