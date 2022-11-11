from django import forms
from .models import Restaurants

class RestaurantSearchForm(forms.ModelForm):
      class Meta:
        model = Restaurants
        fields = ['name', 'cuisine_type']
