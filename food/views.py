from django.shortcuts import render
from summary.views import FoodItemView
from .models import Food
from rest_framework import viewsets
from .forms import FoodForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from summary.serializers import FoodSerializer
from rest_framework.views import  APIView
from rest_framework.views import Response, status

# Create your views here.

class FoodSearchView(APIView):
    serializer_class = FoodSerializer


    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset.exists():
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "No data to show"}, status=status.HTTP_204_NO_CONTENT)

    def get_queryset(self):
        queryset = Food.objects.all()
        name_name = self.request.GET.get('name', '')

        if name_name:
            queryset = queryset.filter(name__unaccent__icontains=name_name)

        return queryset


class FoodAddView(CreateView):
    model = Food
    form_class = FoodForm
    template_name = 'food_form.html'
    success_url = reverse_lazy('food_list')