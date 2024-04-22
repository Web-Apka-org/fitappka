from django.urls import path
from .views import*

urlpatterns = [
    path('', SummaryView.as_view(), name = 'summary'),
    
]