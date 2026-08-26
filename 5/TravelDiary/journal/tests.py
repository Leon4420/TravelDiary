"""Автоматические тесты основных сценариев дневника путешествий."""

from datetime import date
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Travel


class TravelTests(TestCase):
    """Проверяет просмотр, создание и права владельца записи."""

    def setUp(self):
        """Создаёт пользователей и путешествия для выполнения тестов."""
        self.alice = User.objects.create_user("alice", "alice@example.com", "StrongPass123")
        self.bob = User.objects.create_user("bob", "bob@example.com", "StrongPass123")
        self.alice_travel = Travel.objects.create(
            author=self.alice,
            title="Поездка в Берлин",
            country="Германия",
            city="Берлин",
            start_date=date(2026, 5, 1),
            end_date=date(2026, 5, 5),
            cost=Decimal("70000.00"),
            heritage_sites="Музейный остров",
            places_to_visit="Рейхстаг, Тиргартен",
            notes="Краткое описание путешествия.",
        )
        self.bob_travel = Travel.objects.create(
            author=self.bob,
            title="Выходные в Праге",
            country="Чехия",
            city="Прага",
            start_date=date(2026, 6, 10),
            end_date=date(2026, 6, 12),
            cost=Decimal("45000.00"),
            heritage_sites="Исторический центр",
            places_to_visit="Карлов мост",
            notes="Описание поездки другого пользователя.",
        )

    def test_travel_list_is_public(self):
        """Проверяет просмотр общего дневника без входа."""
        response = self.client.get(reverse("travel_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.alice_travel.title)
        self.assertContains(response, self.bob_travel.title)

    def test_detail_contains_required_information(self):
        """Проверяет вывод стоимости и двух списков мест."""
        response = self.client.get(reverse("travel_detail", args=[self.alice_travel.pk]))
        self.assertContains(response, "70000")
        self.assertContains(response, "Музейный остров")
        self.assertContains(response, "Рейхстаг")

    def test_authenticated_user_can_create_travel(self):
        """Проверяет создание путешествия текущим пользователем."""
        self.client.login(username="alice", password="StrongPass123")
        response = self.client.post(
            reverse("travel_create"),
            {
                "title": "Летняя поездка",
                "country": "Италия",
                "city": "Рим",
                "start_date": "2026-07-01",
                "end_date": "2026-07-07",
                "cost": "90000.00",
                "heritage_sites": "Колизей",
                "places_to_visit": "Ватикан, Пантеон",
                "notes": "Описание новой поездки.",
            },
        )
        travel = Travel.objects.get(title="Летняя поездка")
        self.assertRedirects(response, travel.get_absolute_url())
        self.assertEqual(travel.author, self.alice)

    def test_invalid_date_order_is_rejected(self):
        """Проверяет запрет даты окончания раньше даты начала."""
        self.client.login(username="alice", password="StrongPass123")
        response = self.client.post(
            reverse("travel_create"),
            {
                "title": "Ошибка дат",
                "country": "Италия",
                "city": "Рим",
                "start_date": "2026-07-10",
                "end_date": "2026-07-01",
                "cost": "1000.00",
                "heritage_sites": "Колизей",
                "places_to_visit": "Пантеон",
                "notes": "Описание.",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Travel.objects.filter(title="Ошибка дат").exists())

    def test_my_travels_contains_only_owner_records(self):
        """Проверяет состав личного списка путешествий."""
        self.client.login(username="alice", password="StrongPass123")
        response = self.client.get(reverse("my_travels"))
        self.assertContains(response, self.alice_travel.title)
        self.assertNotContains(response, self.bob_travel.title)

    def test_non_owner_cannot_edit_or_delete(self):
        """Проверяет запрет изменения и удаления чужой записи."""
        self.client.login(username="bob", password="StrongPass123")
        edit_response = self.client.get(reverse("travel_update", args=[self.alice_travel.pk]))
        delete_response = self.client.post(reverse("travel_delete", args=[self.alice_travel.pk]))
        self.assertEqual(edit_response.status_code, 403)
        self.assertEqual(delete_response.status_code, 403)
        self.assertTrue(Travel.objects.filter(pk=self.alice_travel.pk).exists())

    def test_owner_can_update_travel(self):
        """Проверяет редактирование путешествия его владельцем."""
        self.client.login(username="alice", password="StrongPass123")
        response = self.client.post(
            reverse("travel_update", args=[self.alice_travel.pk]),
            {
                "title": "Обновлённая поездка в Берлин",
                "country": self.alice_travel.country,
                "city": self.alice_travel.city,
                "start_date": "2026-05-01",
                "end_date": "2026-05-05",
                "cost": "75000.00",
                "heritage_sites": self.alice_travel.heritage_sites,
                "places_to_visit": self.alice_travel.places_to_visit,
                "notes": self.alice_travel.notes,
            },
        )
        self.alice_travel.refresh_from_db()
        self.assertRedirects(response, self.alice_travel.get_absolute_url())
        self.assertEqual(self.alice_travel.cost, Decimal("75000.00"))

    def test_owner_can_delete_travel(self):
        """Проверяет удаление путешествия его владельцем."""
        self.client.login(username="alice", password="StrongPass123")
        self.client.post(reverse("travel_delete", args=[self.alice_travel.pk]))
        self.assertFalse(Travel.objects.filter(pk=self.alice_travel.pk).exists())

    def test_registration_creates_user(self):
        """Проверяет создание нового пользователя системы."""
        response = self.client.post(
            reverse("register"),
            {
                "username": "traveler",
                "email": "traveler@example.com",
                "password1": "StrongPass456",
                "password2": "StrongPass456",
            },
        )
        self.assertRedirects(response, reverse("travel_list"))
        self.assertTrue(User.objects.filter(username="traveler").exists())
