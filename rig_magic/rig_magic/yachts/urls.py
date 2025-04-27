from django.urls import path

from rig_magic.yachts.views import dashboard

app_name = "yachts"

urlpatterns = [
    path("", view=dashboard, name="dashboard"),
]