from django.urls import path
from .views import ConsumedFoodView

urlpatterns = [
    path('consumed_food/', ConsumedFoodView.as_view())
#     path('/', ), # lista Jedzenia w bazie danych
#     path('/<int:pk>/', ),
#     path('/<int:pk>/microelements/', ),
#     path('/<int:pk>/macroelements/', ),
#     path('/<int:pk>/vitamins/', ),
]
