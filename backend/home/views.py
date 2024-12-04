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




@csrf_exempt  
def save_slider_data(request):
    if request.method == "POST":
        print("Request received:", request.body)
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)

            # Check if reset flag is present
            reset = data.get("reset", False)

            if reset:
                # If reset flag is true, we reset the sliders (or perform any reset logic)
                print("Reset action triggered")

            # Extract sliders or autoSimulate flag from the data
            sliders = data.get("sliders")
            auto_simulate = data.get("autoSimulate", False)

            # Ensure folder exists for saving the JSON file
            folder_path = os.path.join(os.getcwd(), "slider_data")
            os.makedirs(folder_path, exist_ok=True)

            # Define file path for saving JSON
            file_path = os.path.join(folder_path, "slider_data.json")

            # Save the slider data (or reset) to a file
            with open(file_path, "w") as json_file:
                json.dump(data, json_file, indent=4)

            return JsonResponse({"message": "Data successfully saved."}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)

    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
