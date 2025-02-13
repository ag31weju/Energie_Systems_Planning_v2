import json, math, random, copy


def process_response():
    prodCapacities = [] 
    autoSimulate = None
    reset = None
    node_data = None,
    bestIdx = []

    with open("slider_data/slider_data.json", "r") as sliderData:
        json_data = json.load(sliderData)
        node_data = json_data.get("nodes")
        slider_data = json_data.get("sliderData")

        prodCapacities = [capacity for capacity in slider_data.get("prodCapacities")]
        autoSimulate = slider_data.get("autoSimulate")
        reset = slider_data.get("reset")
    

    if not reset: 
        if autoSimulate:
            prodCapacities = [[x[0], 0] for x in prodCapacities] #reset prodCapacities to 0

            data = initializeNDarray(len(prodCapacities))

            mainData = fillWholeStructure(data, prodCapacities, bestIdx, node_data)
            data = {"mainData": mainData, "bestIdx": bestIdx}

            #just for testing
            with open('slider_data/tmp.json', 'w') as file:
                  json.dump(data, file, indent=4)
        else:
            data = {"mainData": fill_cell(node_data), "bestIdx": bestIdx}
    else:
        data = {"mainData": initializeNDarray(len(prodCapacities)), "bestIdx": bestIdx}
    

    return data


def initializeNDarray(length):
        #6 is the amount of steps that can be taken in the slider
        return [initializeNDarray(length-1) for _ in range(6)] if length != 0 else None    


def fill_cell(node_data):
        matrixData = math.floor(random.uniform(0, 100))
        lineChartData = {}
        barChartData = {}

        for node in node_data:
            if node.get("type") != "junction":
                 barChartData.update({node.get("id")[-1:]: [math.floor(random.random() * 100) for _ in range(25)]})
                 if node.get("type") == "battery":
                    lineChartData.update({node.get("id")[-1:]: [math.floor(random.random() * 100) for _ in range(25)]})

        return {"matrixData": matrixData,
                "chartsData": {
                    "lineChartData": lineChartData,
                    "barChartData": barChartData,
                    },
                }


def fillWholeStructure(data, prodCapacities, bestIdx, node_data):
    #[float("inf")] since it acts as a mutable container for the bestMatrixVal
    bestMatrixVal = [float("inf")]

    def recFillWholeStructure(pointer, prodCapacities, rec_depth):
        if rec_depth == len(prodCapacities):
            value = fill_cell(node_data)
            if bestMatrixVal[0] > value["matrixData"]: 
                bestMatrixVal[0] = value["matrixData"]
                bestIdx[:] = copy.deepcopy(prodCapacities)
            return value
        else:
            while prodCapacities[rec_depth][1] <= 5:
                pointer[prodCapacities[rec_depth][1]] = recFillWholeStructure(pointer[prodCapacities[rec_depth][1]], prodCapacities, rec_depth+1)
                prodCapacities[rec_depth][1] += 1
            prodCapacities[rec_depth][1] = 0
        return pointer
    
    result = recFillWholeStructure(data, prodCapacities, 0)
    return result