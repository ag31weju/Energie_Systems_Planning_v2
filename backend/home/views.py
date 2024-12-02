from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os


# Create your views here.
def index(request):
    return render(request, "home/index.html")


# post request from frontend
@csrf_exempt  # Only use for testing; use CSRF protection in production!
def process_scenario(request):
    if request.method == "POST":
        try:
            # Parse JSON data from the request
            data = json.loads(request.body)

            # Define the folder path relative to the current directory
            folder_path = os.path.join(os.getcwd(), "scenario")

            # Ensure the folder exists
            os.makedirs(folder_path, exist_ok=True)

            # Define the file path where the JSON will be saved
            file_path = os.path.join(folder_path, "new_file.json")

            # Save the JSON data to the file
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

            processed_data = {"received": data, "message": "Greetings from the backend"}
            return JsonResponse(processed_data, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return JsonResponse({"error": "Invalid HTTP method"}, status=405)
