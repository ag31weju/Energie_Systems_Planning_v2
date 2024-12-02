from django.urls import path
from . import views
from .views import process_scenario

#urls for home app
urlpatterns = [
    path('', views.index, name='index'),
    path('api/process-scenario/', process_scenario, name='process_scenario') #url for api requests
]
