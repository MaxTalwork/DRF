from rest_framework.test import APITestCase
from rest_framework import status

from materials.models import Course, Lesson
from users.models import User
from django.urls import reverse


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="КурсТест", owner=self.user)
        self.lesson = Lesson.objects.create(name="УрокТест", course=self.course, owner=self.user, link="https://www.youtube.com/")
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"name": "КурсТестАпдейт"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "КурсТестАпдейт")

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {"name": "TestCreate1", "link": "https://www.youtube.com/"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)
