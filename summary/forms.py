from django import forms
from food.models import*
from django.utils import timezone

class FoodSummaryForm1(forms.ModelForm):
    date_eating = forms.DateTimeField(initial=timezone.now)
    class Meta:
        model = Food
        fields = '__all__'
        null = True

    def __init__(self, *args, **kwargs):
        super(FoodSummaryForm1, self).__init__(*args, **kwargs)
        self.fields['date_eating'].queryset = ConsumedFood.objects.all().values_list('date_eating', flat=True).distinct()

