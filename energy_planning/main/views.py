from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')  # Use the project-level templates/home.html