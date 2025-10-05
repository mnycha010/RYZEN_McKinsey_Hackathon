from django.urls import path
from . import views

app_name = "member"

urlpatterns = [
    path("onboard/", views.onboard_view, name="onboard"),
]
