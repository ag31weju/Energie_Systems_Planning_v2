import json, math, random, copy


def process_response():
    prodCapacities = [] 
    autoSimulate = None
    reset = None
    bestIdx = []

    with open("slider_data/slider_data.json", "r") as sliderData:
        json_data = json.load(sliderData)
        prodCapacities = [capacity for capacity in json_data.get("prodCapacities")]
        autoSimulate = json_data.get("autoSimulate")
        reset = json_data.get("reset")

    if not reset: 
        if autoSimulate:
            prodCapacities = [[x[0], 0] for x in prodCapacities] #reset prodCapacities to 0

            data = initializeNDarray(len(prodCapacities))

            mainData = fillWholeStructure(data, prodCapacities, bestIdx)
            data = {"mainData": mainData, "bestIdx": bestIdx}

            #just for testing
            #with open('slider_data/tmp.json', 'w') as file:
                  #json.dump(data, file, indent=4)
        else:
            data = {"mainData": fill_cell(), "bestIdx": bestIdx}
    else:
        data = {"mainData": initializeNDarray(len(prodCapacities)), "bestIdx": bestIdx}
    

    return data


def initializeNDarray(length):
        #6 is the amount of steps that can be taken in the slider
        return [initializeNDarray(length-1) for _ in range(6)] if length != 0 else None    


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


def fillWholeStructure(data, prodCapacities, bestIdx):
    #[float("inf")] since it acts as a mutable container for the bestMatrixVal
    bestMatrixVal = [float("inf")]

    def recFillWholeStructure(pointer, prodCapacities, rec_depth):
        if rec_depth == len(prodCapacities):
            value = fill_cell()
            if bestMatrixVal[0] > value["matrixData"]: 
                bestMatrixVal[0] = value["matrixData"]
                print(bestIdx, prodCapacities)
                bestIdx[:] = copy.deepcopy(prodCapacities)
                print(bestIdx, prodCapacities)
            return value
        else:
            while prodCapacities[rec_depth][1] <= 5:
                pointer[prodCapacities[rec_depth][1]] = recFillWholeStructure(pointer[prodCapacities[rec_depth][1]], prodCapacities, rec_depth+1)
                prodCapacities[rec_depth][1] += 1
            prodCapacities[rec_depth][1] = 0
        return pointer
    
    result = recFillWholeStructure(data, prodCapacities, 0)
    print("bestIdx", bestIdx)
    return result