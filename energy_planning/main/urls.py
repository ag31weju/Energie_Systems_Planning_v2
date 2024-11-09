from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Example route
    
    path('say_hello/', views.say_hello, name='say_hello'),
    
]
