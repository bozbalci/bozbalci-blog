from django.urls import path

from notcms.toys import views

app_name = "toys"

urlpatterns = [
    path("barbell/", views.barbell_app, name="barbell-app"),
]
