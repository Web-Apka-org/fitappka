from django.urls import path
from .views import UserRatingView

urlpatterns = [
    path('', UserRatingView.as_view())
]
