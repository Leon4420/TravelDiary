"""Представления учётных записей и пользовательских путешествий."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RegistrationForm, TravelForm
from .models import Travel


def register(request):
    """Регистрирует и авторизует нового пользователя."""
    if request.user.is_authenticated:
        return redirect("travel_list")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("travel_list")
    return render(request, "registration/register.html", {"form": form})


def travel_list(request):
    """Показывает путешествия всех пользователей системы."""
    travels = Travel.objects.select_related("author").all()
    return render(request, "journal/travel_list.html", {"travels": travels})


def travel_detail(request, pk):
    """Показывает подробные сведения о выбранном путешествии."""
    travel = get_object_or_404(Travel.objects.select_related("author"), pk=pk)
    return render(request, "journal/travel_detail.html", {"travel": travel})


@login_required
def my_travels(request):
    """Показывает записи текущего пользователя."""
    travels = Travel.objects.filter(author=request.user)
    return render(request, "journal/my_travels.html", {"travels": travels})


@login_required
def travel_create(request):
    """Создаёт новую запись от имени текущего пользователя."""
    form = TravelForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        travel = form.save(commit=False)
        travel.author = request.user
        travel.save()
        messages.success(request, "Путешествие добавлено.")
        return redirect(travel)
    return render(request, "journal/travel_form.html", {"form": form, "heading": "Новое путешествие"})


@login_required
def travel_update(request, pk):
    """Изменяет путешествие только при наличии прав владельца."""
    travel = get_object_or_404(Travel, pk=pk)
    if travel.author != request.user:
        raise PermissionDenied
    form = TravelForm(request.POST or None, instance=travel)
    if request.method == "POST" and form.is_valid():
        messages.success(request, "Изменения сохранены.")
        return redirect(form.save())
    return render(request, "journal/travel_form.html", {"form": form, "heading": "Редактирование путешествия"})


@login_required
def travel_delete(request, pk):
    """Удаляет путешествие после подтверждения его владельцем."""
    travel = get_object_or_404(Travel, pk=pk)
    if travel.author != request.user:
        raise PermissionDenied
    if request.method == "POST":
        travel.delete()
        messages.success(request, "Путешествие удалено.")
        return redirect("my_travels")
    return render(request, "journal/travel_delete.html", {"travel": travel})
