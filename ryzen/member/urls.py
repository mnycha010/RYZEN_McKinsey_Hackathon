from django.urls import path
from . import views

app_name = "member"

urlpatterns = [
    path("onboard/", views.onboard_view, name="onboard"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("ai-analytics/", views.ai_analytics_view, name="ai_analytics"),
    path("profile/", views.profile_view, name="profile"),
    path("ai-analytics/clear/", views.ai_analytics_clear, name="ai_analytics_clear"),

    path("meetings/", views.meetings_view, name="meetings"),

]
