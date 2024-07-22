from django.urls import path

from .views import RecipiesView

urlpatterns = [
    path('', RecipiesView.as_view())
]
