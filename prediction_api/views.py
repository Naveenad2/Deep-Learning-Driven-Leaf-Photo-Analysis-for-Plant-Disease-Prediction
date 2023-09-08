from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import *
from io import BytesIO
from PIL import Image
import numpy as np
import tensorflow as tf
from .forms import *
from django.http import HttpResponse


POTATTO_MODEL = tf.keras.models.load_model("prediction_api/saved_plant_disease_model")
APPLE_MODEL = tf.keras.models.load_model("prediction_api/apple_saved_plant_disease_model")
GRAPE_POTATTO_MODEL = tf.keras.models.load_model("prediction_api/grape_plant_disease_model")
TOMATTO_POTATTO_MODEL = tf.keras.models.load_model("prediction_api/tomato_saved_plant_disease_model")
PEPPER__MODEL = tf.keras.models.load_model("prediction_api/pepper_saved_plant_disease_model")
STRAWBERRY_MODEL = tf.keras.models.load_model("prediction_api/strawberry_plant_disease_model")
CORN_MODEL = tf.keras.models.load_model("prediction_api/corn_saved_plant_disease_model")

potato = ['Potato Early blight', 'Potato Late blight', 'Potato healthy']

apple = ['Apple Apple scab', 'Apple Black rot', 'Apple Cedar apple rust']

corn = ['Corn(maize) Cercospora leaf spot Gray leaf spot','Corn(maize) Common rust ','Corn(maize) healthy']

grape = ['Grape Black rot',
 'Grape Esca(Black Measles)',
 'Grape Leaf blight(Isariopsis Leaf Spot)']
pepper =['Pepper ell Bacterial spot', 'Pepper bell healthy']
strawberry =['Strawberry Leaf scorch', 'Strawberry healthy']
tomato = ['Tomato Leaf Mold',
 'Tomato Septoria leaf spot',
 'Tomato Spider mites Two spotted spider mite']
# Create your views here.
def Signup(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(username,email,password)
        user = User.objects.filter(username=username).exists()

        if user is False:
                new_user_create = User.objects.create_user(
                    username=username, password=password)
                new_user_create.save()
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('/')
    return render(request, 'store/register.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return HttpResponse("Wrong password")
    return render(request, 'store/login.html')

@login_required(login_url='/Login')
def Index(request):
     user_id = request.user.id
     user_object = User.objects.filter(id=user_id)
     username = ''
     for user in user_object:
          username = user.username
     plants_models_available = Plants.objects.all()
     return render(request, 'store/index.html',{'plants_models_available':plants_models_available,
     'username':username})

@login_required(login_url='/Login')


def Plant_prediction(request,id):

    pre_flag = 0

     
     
    if request.method == "POST":
           
           plant_object = Plants.objects.filter(id=id)
           
           
           form=Plant_image(data=request.POST,files=request.FILES)
           pre_flag = 1

           if form.is_valid():
               form.save()
               obj=form.instance
               print(form.instance.plant_image)

               #get user id
               user_id = request.user.id
               user = User.objects.get(id=user_id)


              

               image_file = open(str(form.instance.plant_image), 'rb')
               image_bytes = image_file.read()
               image_array = np.array(Image.open(BytesIO(image_bytes)))
            
               expand_image_array = np.expand_dims(image_array,0)

               diesease_dis = ''
               ####################################
               if(id==1):
                         prediction = POTATTO_MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = potato[index]
                      

                         
               
               if(id==2):
                         prediction = TOMATTO_POTATTO_MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = tomato[index]
                         
                         
                         
               
               if(id==3):
                         prediction = APPLE_MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = apple[index]
                         
               
               if(id==4):
                        
                         prediction = PEPPER__MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = pepper[index]
               
               if(id==5):
                       
                         prediction = GRAPE_POTATTO_MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = grape[index]
                         
               
               if(id==6):
                         prediction = STRAWBERRY_MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = strawberry[index]
                         
               
               if(id==7):
                         prediction = CORN_MODEL.predict(expand_image_array)
                         index = np.argmax(prediction)
                         diesease = corn[index]
               
               print(diesease)

               model_obj =  User_history(user_id=user,Plants_name=obj.Plants_name,symptom=obj.symptom,predicted_d=diesease,plant_image=str(obj.plant_image))
               model_obj.save()


               return render(request,"store/plant_prediction.html",{"obj":obj,'pre_flag':pre_flag,'diesease':diesease})

    
    plant_object = Plants.objects.filter(id=id)

    form=Plant_image()

    

    return render(request,"store/plant_prediction.html",{"form":form,'plant_object':plant_object})
     


@login_required(login_url='/Login')
def Main_prediction(request):
     
    #f = open('../static/images/pottato.JPG', 'rb')
     #image_bytes = f.read()
     return render(request,'store/prediction_page.html')

@login_required(login_url='/Login')
def User_history_fun(request):
     user_id = request.user.id
     user = User.objects.get(id=user_id)
     history_of_user = User_history.objects.filter(user_id=user)

     return render(request,'store/history.html',{'history':history_of_user})


@login_required(login_url='/Login')
def profile(request):
     user_id = request.user.id
     user = User.objects.filter(id=user_id)
     return render(request,'store/profile.html',{'user':user})

def Delete_user(request):
        user_id = request.user.id
        User.objects.filter(id=user_id).delete()
       # logout(request)

        return render(request, 'store/login.html')


def Logout_(request):
       logout(request)
       return render()