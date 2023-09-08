from django.contrib import admin


from .models import *
# Register your models here.
admin.site.register(Plants)
admin.site.register(Prediction_plant)
admin.site.register(User_history)