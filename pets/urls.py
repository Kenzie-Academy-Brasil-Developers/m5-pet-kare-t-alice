from django.urls import path
from .views import PetView
from .views import PetDetailView

urlpatterns = [
    path("pets/", PetView.as_view()),
    path("pets/<int:pet_id>/", PetDetailView.as_view())
    ]