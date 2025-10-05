from django.urls import path
from . import views

app_name = "member"

urlpatterns = [
    path("onboard/", views.onboard_view, name="onboard"),
    path("dashboard/", views.dashboard_view, name="dashboard"), 
]


