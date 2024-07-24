from django.urls import path
from summary.views import FoodItemView
from .views import FoodSearchView, FoodAddView

urlpatterns = [
     path('', FoodItemView.as_view({'get':'list'}), name = 'food_list'), # lista Jedzenia w bazie danych
     path('search/', FoodSearchView.as_view()),
     path('add', FoodAddView.as_view(), name='add_food')
#     path('/<int:pk>/', ),
#     path('/<int:pk>/microelements/', ),
#     path('/<int:pk>/macroelements/', ),
#     path('/<int:pk>/vitamins/', ),
 ]
