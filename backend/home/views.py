from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .scenario_processing import process_image,parse_json  # Import the external processing method
from PIL import Image, ImageOps
import json
import os, io
import random, math


# Create your views here.
def index(request):
    return render(request, "home/index.html")


# post request from frontend
@csrf_exempt  # Only use for testing; use CSRF protection in production!
def process_scenario(request):
    if request.method == "GET":
        try:
            # request holds ID for scenario selection
            id = request.GET.get("id")
            filetype = request.GET.get("filetype")
            print(id, filetype)

            if not id:
                return JsonResponse({"error": "Missing 'id' parameter"}, status=400)

            if not filetype:
                return JsonResponse(
                    {"error": "Missing 'filetype' parameter"}, status=400
                )

            # Define the folder path relative to the current working directory
            folder_path = f"scenario/scenario{id}"

            if filetype == "json":
                graph_path = f"{folder_path}/graph.json"  # path for graph.json
                if not os.path.exists(graph_path):
                    return JsonResponse({"error": "Graph file not found"}, status=404)

                with open(
                    graph_path, "r"
                ) as graph:  # open the file so that it can be read
                    data = json.load(
                        graph
                    )  # deserializes opened json file to actual data that can be sent as a JsonResponse
                    return JsonResponse(data, status=200)

            if filetype == "png":
                img_path = f"{folder_path}/img.png"  # path for img.png
                if not os.path.exists(img_path):
                    return JsonResponse({"error": "Image file not found"}, status=404)

                with open(img_path, "rb") as img:
                    response = HttpResponse(
                        img.read(), content_type="image/png"
                    )  # Creates HTTPResponse with the binary data of the image
                    response["Content-Disposition"] = (
                        "attachment; filename=img.png"  # tells the frontend that the file should be treated as a download and not displayed
                    )
                    return response
            else:
                return JsonResponse(
                    {"error": "Invalid 'filetype' parameter. Use 'json' or 'png'."},
                    status=400,
                )

        except Exception as e:
            return JsonResponse(
                {f"error when trying to open and process data: {e}"}, status=500
            )
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
    elif request.method == "GET":
        # Use the gotten Slider data for some computation with the optimizer

        prodCapacities = []
        autoSimulate = None
        reset = None
        

        with open("slider_data/slider_data.json", "r") as sliderData:
            json_data = json.load(sliderData)
            prodCapacities = [capacity for capacity in json_data.get("prodCapacities")]
            autoSimulate = json_data.get("autoSimulate")
            reset = json_data.get("reset")

        print(prodCapacities)
        
        def fill_cell():
            return {"matrixData": math.floor(random.uniform(0, 100)) ,
                    "chartsData": {
                        "lineChartData": [math.floor(random.random() * 100) for _ in range(25)],
                        "barChartData": {
                            "purchased_power": [math.floor(random.random() * 100) for _ in range(25)],
                            "pv_production": [math.floor(random.random() * 100) for _ in range(25)],
                            "pv_curtailment": [math.floor(random.random() * 100) for _ in range(25)],
                            "storage_charge": [math.floor(random.random() * 100) for _ in range(25)],
                            "storage_discharge": [math.floor(random.random() * 100) for _ in range(25)],
                            "demand": [math.floor(random.random() * -100) for _ in range(25)],
                            },
                        },
                    }

        bestIdx = []
        def fillWholeStructure(pointer, prodCapacities, rec_depth, bestMatrixVal):
            if rec_depth == len(prodCapacities):
                value = fill_cell()
                if bestMatrixVal[0] > value["matrixData"]: 
                    bestMatrixVal[0] = value["matrixData"]
                    bestIdx[:] = prodCapacities[:]
                return value
            else:
                while prodCapacities[rec_depth] <= 5:
                    pointer[prodCapacities[rec_depth]] = fillWholeStructure(pointer[prodCapacities[rec_depth]], prodCapacities, rec_depth+1, bestMatrixVal)
                    prodCapacities[rec_depth] += 1
                prodCapacities[rec_depth] = 0
            return pointer
        
        def initializeNDarray(length):
            #6 is the amount of steps that can be taken in the slider
            return [initializeNDarray(length-1) for _ in range(6)] if length != 0 else None
        
        #Start filling the data structure on autosimulate, otherwise return a simple object. If reset is true, then don't do anything
        if not reset: 
            if autoSimulate:
                prodCapacities = [0 for x in prodCapacities] #reset prodCapacities to 0

                data = initializeNDarray(len(prodCapacities))
                #[float("inf")] since it acts as a mutable container for the bestMatrixVal
                data = {"mainData": fillWholeStructure(data, prodCapacities, 0, [float("inf")]), "bestIdx": bestIdx}

                #just for testing
                #with open('slider_data/tmp.json', 'w') as file:
                 #   json.dump(data, file, indent=4)
            else:
               data = {"mainData": fill_cell(), "bestIdx": bestIdx}
        else:
            data = {"mainData": initializeNDarray(len(prodCapacities)), "bestIdx": bestIdx}


        return JsonResponse(data, status=200)
    return JsonResponse({"error": "Invalid HTTP method."}, status=405)

@csrf_exempt  
def save_scenario(request):
    if request.method == 'POST':
        try:
            # Parse the incoming JSON data
            data = json.loads(request.body)
            nodes = data.get('nodes')
            edges = data.get('edges')
            image_url = data.get('imageUrl')

            folder_path = os.path.join(os.getcwd(), "scenario_data")
            os.makedirs(folder_path, exist_ok=True)

            # Define file path for saving JSON
            file_path = os.path.join(folder_path, "scenario_data.json")
            
            with open(file_path, 'w') as f:
                json.dump(data, f)

           

            return JsonResponse({"status": "success", "message": "Data saved successfully."}, status=200)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

#Scenario upload: gets an image, crops it and sends it back as response to be displayed, Json file is also recieved-> printed out for now
@csrf_exempt  # Use CSRF protection in production
def upload_files(request):
    if request.method == "POST" and request.FILES:
        try:
            # Get the uploaded files
            image = request.FILES.get("image")
            json_file = request.FILES.get("json")

            # Parse the JSON file
            json_data = parse_json(json_file)
            
            # Add your logic to process the JSON file here

            if not image:
                return JsonResponse({"error": "No image file provided"}, status=400)

            # Call the external image processing function
            processed_image_io = process_image(image)

            # Return the processed image in the response
            response = HttpResponse(processed_image_io, content_type="image/png")
            response["Content-Disposition"] = 'attachment; filename="cropped_image.png"'
            #could add json to response as well, not needed though
            return response

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

