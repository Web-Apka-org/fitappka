from django.urls import path
from .views import TokenView, RefreshTokenView, UserDataView, RegisterView

urlpatterns = [
    path('', UserDataView.as_view()),
    path('token/', TokenView.as_view()),
    path('token/refresh/', RefreshTokenView.as_view()),
    path('register/', RegisterView.as_view()),
]
