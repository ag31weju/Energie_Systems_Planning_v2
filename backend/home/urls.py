from django.urls import path
from . import views
#urls for home app
urlpatterns = [
    path('', views.index, name='index'),
]
