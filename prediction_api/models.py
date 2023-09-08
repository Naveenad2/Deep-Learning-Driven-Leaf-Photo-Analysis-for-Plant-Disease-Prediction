from django.db import models

from distutils.command.upload import upload
from msilib import CAB
from pyexpat import model
from django.forms import ImageField
from django.contrib.auth.models import User


# Create your models here.
class Plants(models.Model):
    Plants_name = models.CharField(max_length=30)
    Plant_discription = models.TextField(max_length=150)
    plant_model_image = models.ImageField(upload_to='./static/images')
    model_accuracy = models.IntegerField()
    model_file = models.FileField(upload_to='./saved_plant_disease_model/model')
    
    def __str__(self):
        return self.Plants_name

class Prediction_plant(models.Model):
     Plants_name = models.CharField(max_length=30)
     symptom = models.CharField(max_length=50)
     plant_image = models.ImageField(upload_to='./static/images')
     predicted_d = models.CharField(max_length=50)
     user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

     def __str__(self):
         
         return self.Plants_name
     
class User_history(models.Model):
     
     Plants_name = models.CharField(max_length=30)
     symptom = models.CharField(max_length=50)
     plant_image = models.CharField(max_length=300)
     predicted_d = models.CharField(max_length=50)
     user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True)

     def __str__(self):
         
         return self.Plants_name