from django.db import models  
from django.forms import fields  

from django import forms 
from .models import * 

class Plant_image(forms.ModelForm):
    class Meta:
        model = Prediction_plant 

        fields = ('Plants_name', 'symptom','plant_image')
