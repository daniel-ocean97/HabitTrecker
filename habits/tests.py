from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitViewSetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass"
        )

        # Привычки для тестового пользователя
        self.habit1 = Habit.objects.create(
            user=self.user, place="Дом", time="12:00:00", action="Чтение", duration=60
        )

        # Привычка другого пользователя
        self.habit2 = Habit.objects.create(
            user=self.other_user,
            place="Офис",
            time="13:00:00",
            action="Прогулка",
            duration=120,
        )

    def test_habit_list_authenticated(self):
        """Только свои привычки для аутентиф. пользователя"""
        self.client.force_authenticate(user=self.user)
        url = "/api/habits/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_habit_create_assigns_owner(self):
        self.client.force_authenticate(user=self.user)
        url = "/api/habits/"

        # Данные без user
        data = {
            "place": "Парк",
            "time": "14:00:00",
            "action": "Бег",
            "is_pleasant": False,
            "periodicity": 1,
            "duration": 90,
        }

        response = self.client.post(url, data, format="json")

        # Проверки
        self.assertEqual(response.status_code, 201)


class PublicHabitTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

        # Публичные и приватные привычки
        self.public_habit = Habit.objects.create(
            user=self.user,
            place="Кафе",
            time="09:00:00",
            action="Кофе",
            duration=60,
            is_public=True,
        )
        self.private_habit = Habit.objects.create(
            user=self.user, place="Спальня", time="23:00:00", action="Сон", duration=120
        )

    def test_public_list_without_auth(self):
        """Список публичных привычек недоступен без авторизации"""
        url = "/public-habits/"  # прямой URL для списка
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_public_detail_access(self):
        """Детали публичной привычки без аутентификации"""
        url = f"/public-habits/{self.public_habit.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_private_detail_blocked(self):
        """Приватные привычки недоступны публично"""
        url = f"/public-habits/{self.public_habit.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
