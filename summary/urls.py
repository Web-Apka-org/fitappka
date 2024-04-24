from django.urls import path
from .views import*

urlpatterns = [
    path('', FoodItemView.as_view({'get':'list'}), name = 'summary'),
    path('add-food-summary/', AddFoodSummaryView1.as_view(), name='add-food-summary1'),

]