from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='matchapp-home'),
    path('about/', views.about, name='matchapp-about'),
]