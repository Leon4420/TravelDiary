"""Модель пользовательской записи о путешествии."""

from decimal import Decimal

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Travel(models.Model):
    """Хранит основные сведения и впечатления о путешествии."""

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="travels")
    title = models.CharField(max_length=160)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))])
    heritage_sites = models.TextField()
    places_to_visit = models.TextField()
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Выводит последние добавленные путешествия первыми."""

        ordering = ["-created_at"]

    def __str__(self):
        """Возвращает название путешествия и имя пользователя."""
        return f"{self.title} — {self.author.username}"

    def get_absolute_url(self):
        """Возвращает URL-адрес страницы путешествия."""
        return reverse("travel_detail", args=[self.pk])

    @property
    def duration_days(self):
        """Возвращает продолжительность путешествия в днях."""
        return (self.end_date - self.start_date).days + 1
