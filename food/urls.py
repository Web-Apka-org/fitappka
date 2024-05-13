from django.urls import path, re_path
from .views import ConsumedFoodView

urlpatterns = [
    path('consumed/', ConsumedFoodView.as_view()),
#     path('/', ), # lista Jedzenia w bazie danych
#     path('/<int:pk>/', ),
#     path('/<int:pk>/microelements/', ),
#     path('/<int:pk>/macroelements/', ),
#     path('/<int:pk>/vitamins/', ),
]
