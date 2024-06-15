from django.urls import path
from .views import UserTokenView

urlpatterns = [
#     path('/', ), # rest api: informacje o użytkowniku
    path('token/', UserTokenView.as_view()),
#     path('/logout/', ),
#     path('/signup/', ),
]
