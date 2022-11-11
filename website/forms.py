from django.forms import ModelForm
from django import forms
from .models import Orders
from .models import Restaurants

class OrderForm(ModelForm):
	class Meta:
		model = Orders
		fields = '__all__'
		


class RestaurantSearchForm(forms.ModelForm):
      class Meta:
        model = Restaurants
        fields = ['name', 'cuisine_type']