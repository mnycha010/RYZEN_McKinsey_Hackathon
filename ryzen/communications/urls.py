from django.urls import path
from . import views

app_name = "communications"

urlpatterns = [
    path("coordinators/", views.coordinators_view, name="coordinators"),
    path("notifications/", views.notifications_view, name="notifications"),
]
