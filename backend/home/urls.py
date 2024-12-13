from django.urls import path
from . import views
from .views import process_scenario
from .views import save_slider_data

#urls for home app
urlpatterns = [
    path('', views.index, name='index'),
    path('api/process-scenario/', process_scenario, name='process_scenario'),
    path('api/save-slider-data/', save_slider_data, name='save_slider_data'), #url for api requests
    path('api/save-scenario/', views.save_scenario, name='save_scenario'),
]
