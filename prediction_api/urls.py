import imp
from django.urls import path
from . import views

from django.conf import settings
from django.urls import  re_path
from django.views.static import serve


 
urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),

    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('', views.Index, name='Index'),
    path('Login', views.Login, name='Login'),
    path('Register',views.Signup,name='Signup'),
    path('plant_prediction/<int:id>',views.Plant_prediction,name='Plant_prediction'),
    path('plant_prediction/predction',views.Main_prediction,name='Main_prediction'),
    path('history',views.User_history_fun,name='User_history_fun'),
    path('pro',views.profile,name='profile'),
    path('del',views.Delete_user,name='Delete_user'),
    path('logout',views.Logout_,name='Logout_')

]