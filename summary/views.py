from django.shortcuts import render
from rest_framework.views import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from food.models import Food
from .serializers import *
from django.views.generic.edit import CreateView
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Sum
from django.utils.dateparse import parse_datetime

'''
/summary/GET
Zwraca sumę wartości odżywczych wszystkich posiłków 
zjedzonych w tym miesiącu. Niech nie zwraca danych, 
które są zerowe (np: protein = 0).
'''

'''
/summary/?from=<data>&to=<data>
GET
zwraca sumę wartości odżywczych w danym przedziale czasowym.
'''

'''
jeśli będzie podane tylko from, wtedy od from do dnia dzisiejszego. 
jeśli tylko 'to' to zwraca sumę wartości z dnia podanego w 'to'
'''


class FoodItemView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    model = Food
    serializer_class = FoodSerializer

    def get_queryset(self):
        consumed_foods =ConsumedFood.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        queryset = Food.objects.none()
        if start_date and end_date:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            if start_date and end_date:
                
                consumed_foods = consumed_foods.filter(date_eating__range=[start_date, end_date])
                if consumed_foods.exists():
                    queryset = Food.objects.all()
                    food_ids = consumed_foods.values_list('food', flat=True)
                    queryset = Food.objects.filter(id__in=food_ids)
                else:
 
                    return queryset  # Return an empty queryset
            else:

                return queryset

        return queryset
    def list(self, request, *args, **kwargs):
        id = self.request.user.id
        queryset = self.get_queryset()

        if id == self.request.user.id and queryset:
            aggregates = queryset.aggregate(energy = Sum('energy'),fat = Sum('fat'),saturated_fat = Sum('saturated_fat'))

            
            serializer = self.get_serializer(queryset, many = True)
            
            response_data = {
                'result':aggregates,
                'foods':serializer.data
            ,
            }
            return Response(response_data)
        return Response("No data to show")
    
class AddFoodSummaryView1(CreateView):
    model = ConsumedFood
    blank = True
    form_class = FoodSummaryForm1
    template_name = 'add_food_summary.html'
    success_url = reverse_lazy('summary')

