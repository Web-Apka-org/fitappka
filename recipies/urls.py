from django.urls import path

from .views import Recipies, RecipiesUpdate

urlpatterns = [
    path('', Recipies.as_view()),
    path('update/', RecipiesUpdate.as_view())
]
