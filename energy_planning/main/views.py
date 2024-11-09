from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def home(request):
    return render(request, 'main/home.html')




def say_hello(request):
    data = {"message": "Hello World"}
    return JsonResponse(data)
