from django.shortcuts import render
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from .models import FoodSummary
from account.models import User 
from .serializers import SummarySerializer
# Create your views here.

'''
/summary/GET
Zwraca sumę wartości odżywczych wszystkich posiłków 
zjedzonych w tym miesiącu. Niech nie zwraca danych, 
które są zerowe (np: protein = 0).
'''
class SummaryView(APIView):
    model = FoodSummary
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user_id = self.request.user.id
            id = kwargs.get('id')
            if user_id == self.request.user.id:
                data = FoodSummary.objects.all()
                serializer = SummarySerializer(data, many = True)
                return Response(serializer.data)
            else:
                return Response({'error': 'You do not have permission to view this user data.'}, status=403)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
'''
/summary/?from=<data>&to=<data>
GET
zwraca sumę wartości odżywczych w danym przedziale czasowym.
'''

'''
jeśli będzie podane tylko from, wtedy od from do dnia dzisiejszego. 
jeśli tylko 'to' to zwraca sumę wartości z dnia podanego w 'to'
'''