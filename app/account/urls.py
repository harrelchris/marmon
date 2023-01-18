from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("delete/", views.delete, name="delete"),
    path("settings/", views.settings_view, name="settings"),
]
