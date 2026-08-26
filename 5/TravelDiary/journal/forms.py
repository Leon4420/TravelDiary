"""Формы регистрации и редактирования путешествий."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Travel


class RegistrationForm(UserCreationForm):
    """Создаёт пользователя с обязательной электронной почтой."""

    email = forms.EmailField(label="Электронная почта", required=True)

    class Meta(UserCreationForm.Meta):
        """Определяет поля формы регистрации."""

        model = User
        fields = ("username", "email", "password1", "password2")


class TravelForm(forms.ModelForm):
    """Создаёт или изменяет запись о путешествии."""

    class Meta:
        """Определяет поля и элементы формы путешествия."""

        model = Travel
        fields = (
            "title",
            "country",
            "city",
            "start_date",
            "end_date",
            "cost",
            "heritage_sites",
            "places_to_visit",
            "notes",
        )
        labels = {
            "title": "Название путешествия",
            "country": "Страна",
            "city": "Город или регион",
            "start_date": "Дата начала",
            "end_date": "Дата окончания",
            "cost": "Стоимость путешествия",
            "heritage_sites": "Места культурного наследия",
            "places_to_visit": "Места для посещения",
            "notes": "Описание и впечатления",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "heritage_sites": forms.Textarea(attrs={"rows": 4}),
            "places_to_visit": forms.Textarea(attrs={"rows": 4}),
            "notes": forms.Textarea(attrs={"rows": 7}),
        }

    def clean(self):
        """Проверяет правильный порядок дат путешествия."""
        cleaned = super().clean()
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        if start_date and end_date and end_date < start_date:
            self.add_error("end_date", "Дата окончания не может быть раньше даты начала.")
        return cleaned
