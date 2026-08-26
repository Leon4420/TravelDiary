"""Маршруты приложения дневника путешествий."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.travel_list, name="travel_list"),
    path("register/", views.register, name="register"),
    path("my-travels/", views.my_travels, name="my_travels"),
    path("travels/new/", views.travel_create, name="travel_create"),
    path("travels/<int:pk>/", views.travel_detail, name="travel_detail"),
    path("travels/<int:pk>/edit/", views.travel_update, name="travel_update"),
    path("travels/<int:pk>/delete/", views.travel_delete, name="travel_delete"),
]
