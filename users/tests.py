from rest_framework.test import APITestCase
from rest_framework import status
from materials.models import Course
from users.models import User, Subscription
from django.urls import reverse


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name="КурсТест", owner=self.user)
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)

    def test_subscribe(self):
        Subscription.objects.all().delete()
        url = reverse("users:subscription")
        data = {'course': self.course.pk}
        response = self.client.post(url, data)
        data = response.json()
        # print(response.json)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('message'), 'Подписка включена')
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())
