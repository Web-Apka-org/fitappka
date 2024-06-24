from django.urls import path
from .views import TokenView, RefreshTokenView

urlpatterns = [
#     path('/', ), # rest api: informacje o użytkowniku
    path('token/', TokenView.as_view()),
    path('token/refresh/', RefreshTokenView.as_view()),
#     path('/signup/', ),
]
