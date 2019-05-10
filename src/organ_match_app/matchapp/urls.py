from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='matchapp-home'),
    path('about/', views.about, name='matchapp-about'),
    path('request/', views.request_organ, name='matchapp-request'),
    path('offer/', views.offer_organ, name='matchapp-offer'),
]