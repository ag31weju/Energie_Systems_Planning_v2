<template>
  <div id="drawerbox">
    <Drawerbox></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield></Playfield>
      </div>
      <div id="slider-box">
        <Sliders @getSimulationData="handleSimulationData"></Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix-box" class="grid-column">
        <Matrix
          ref="matrixComp"
          :matrixData="matrixData"
          :matrixTheme="currTheme.matrixTheme"
          :sliderVals="sliderVals"
        ></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts
          ref="chartsComp"
          :chartsData="chartsData"
          :sliderVals="sliderVals"
        ></Charts>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, provide, watch, useTemplateRef } from "vue";
import Chart from "primevue/chart";
import Sliders from "../components/Sliders.vue";
import Playfield from "../components/PlayfieldStudent.vue";
import Matrix from "../components/Matrix.vue";
import Charts from "../components/Charts.vue";
import Drawerbox from "../components/Drawerbox.vue";
import { usedTheme } from "../assets/stores/pageSettings";

export default {
  setup(props, context) {
    const first = ref(true);
    const currTheme = usedTheme();
    const sliderVals = ref([0, 0]);
    const matrixData = ref(undefined);
    const chartsData = ref(undefined);

    const isAutoSimulating = ref(false);
    const stopAutoSimulate = ref(false);
    const newScenarioLoaded = ref(false);

    const selectedNodes = ref([-1, -1]);
    const dataValues = ref(undefined);
    const prodCapacities = ref(undefined);

    provide("selectedNodes", selectedNodes);
    provide("prodCapacities", prodCapacities);
    provide("dataValues", dataValues);
    provide("extractDataValuesCell", extractDataValuesCell);

    const matrixComp = useTemplateRef("matrixComp");
    const chartsComp = useTemplateRef("chartsComp");

    let numberProducers = 0;
    let numberConsumers = 0;

    provide("isAutoSimulating", isAutoSimulating);
    provide("newScenarioLoaded", newScenarioLoaded);
    provide("sliderVals", sliderVals);

    const matrixTheme = ref({ backgroundColor: "white", gridColor: "black" });

    function handleSimulationData(propagateChange) {
      if (selectedNodes.value[0] === -1 || selectedNodes.value[1] === -1)
        return;

      if (propagateChange.reset) {
        isAutoSimulating.value = false;
        stopAutoSimulate.value = true;
        if (!isAutoSimulating.value)
          prepareNewScenario(numberProducers, numberConsumers);
      }
      if (!isAutoSimulating.value) {
        if (propagateChange.autoSimulate) {
          isAutoSimulating.value = true;
          dataValues.value = propagateChange.simData;
          prodCapacities.value.map(() => 0);
          autoSimulateData(propagateChange);
        } else {
          updateDataValuesCell(dataValues.value, propagateChange);
          simulateData(propagateChange, propagateChange.sliderVals);
        }
      }
    }
    async function autoSimulateData(propagateChange) {
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      for (let rowIndex = 0; rowIndex < 6; rowIndex++) {
        for (let colIndex = 0; colIndex < 6; colIndex++) {
          if (stopAutoSimulate.value) {
            stopAutoSimulate.value = false;
            return;
          }
          //Extract desired values from propagateChange.simData or dataValues
          prodCapacities.value[selectedNodes.value[1]] = rowIndex;
          prodCapacities.value[selectedNodes.value[0]] = colIndex;
          let currentSliderVals = [colIndex, rowIndex];
          let cell = {
            simData: getDataValuesCell(propagateChange.simData),
            reset: propagateChange.reset,
            autoSimulate: propagateChange.autoSimulate,
            sliderVals: propagateChange.sliderVals,
            bestIdx: propagateChange.bestIdx,
          };
          simulateData(cell, currentSliderVals);
          //change prodCapacities for currently selected nodes so that the heatmap and charts update visually (even if the values have already been assigned to dataValues)
          await sleep(700);
        }
      }
      sliderVals.value = propagateChange.bestIdx;
      isAutoSimulating.value = false;
    }

    function getDataValuesCell(pointer) {
      for (let i = 0; i < prodCapacities.value.length; i++) {
        if (i === prodCapacities.value.length - 1) {
          console.log(pointer[prodCapacities.value[i]]);
          return pointer[prodCapacities.value[i]];
        }

        if (!pointer) {
          console.error(
            "prodCapacities length is not equal to dataValues depth"
          );
          throw new Error(
            "prodCapacities length is not equal to dataValues depth"
          );
        }

        console.log("i", pointer[prodCapacities.value[i]]);
        pointer = pointer[prodCapacities.value[i]];
      }
    }

    function extractDataValuesCell(
      newZ,
      pointer,
      capacities,
      rec_depth,
      colID,
      rowID,
      colIndex,
      rowIndex,
      forMatrix,
      forCharts
    ) {
      if (rec_depth == capacities.length) {
        return forMatrix
          ? pointer.matrixData
          : forCharts
          ? pointer.chartsData
          : console.error("data cannot be assigned to visualization component");
      } else {
        if (selectedNodes.value.some((el) => el === rec_depth)) {
          if (rec_depth === colID) {
            for (let currColIndex = 0; currColIndex <= 5; currColIndex++) {
              newZ[rowIndex][currColIndex] = extractDataValuesCell(
                newZ,
                pointer[prodCapacities[rec_depth]],
                capacities,
                rec_depth + 1,
                colID,
                rowID,
                colIndex,
                rowIndex
              );
            }
          } else if (rec_depth === rowID) {
            for (let currRowIndex = 0; currRowIndex <= 5; currRowIndex++) {
              newZ[currRowIndex][colIndex] = extractDataValuesCell(
                newZ,
                pointer[prodCapacities[rec_depth]],
                capacities,
                rec_depth + 1,
                colID,
                rowID,
                colIndex,
                rowIndex
              );
            }
          } else {
            console.error("rec_depth does not equal any selected node ID");
          }
        } else {
          extractDataValuesCell(
            newZ,
            pointer[prodCapacities[rec_depth]],
            capacities,
            rec_depth + 1,
            colID,
            rowID,
            colIndex,
            rowIndex
          );
        }
      }
    }

    function updateDataValuesCell(pointer, propagateChange) {
      for (let i = 0; i < prodCapacities.value.length; i++) {
        if (i === prodCapacities.value.length - 1) {
          pointer[prodCapacities[i]] = propagateChange.simData;
          console.log(pointer[prodCapacities[i]]);
          return;
        }

        if (!pointer) {
          console.error(
            "prodCapacities length is not equal to dataValues depth"
          );
          throw new Error(
            "prodCapacities length is not equal to dataValues depth"
          );
        }

        pointer = pointer[prodCapacities.value[i]];
      }
    }

    function simulateData(propagateChange, currentSliderVals) {
      sliderVals.value = currentSliderVals;
      matrixData.value = {
        reset: propagateChange.reset,
        matrixValue: propagateChange.simData.matrixData,
      };
      chartsData.value = {
        reset: propagateChange.reset,
        chartsValues: propagateChange.simData.chartsData,
      };
    }

    function handleNodeSelection(newNode) {
      if (!isAutoSimulating.value) {
        console.log(selectedNodes);
        //LIFO-wise selection -> 0 first, 1 subsequently
        const idx = selectedNodes.value.findIndex((el) => {
          return el === newNode;
        });
        //if idx >= 0, that means that the node is supposed to be de-highlighted (shifted with idx = 0, popped with idx = 1). Otherwise, it is going to be highlighted (pushed)
        if (idx >= 0) {
          idx === 0
            ? (selectedNodes.value = [selectedNodes.value[1], -1])
            : (selectedNodes.value = [selectedNodes.value[0], -1]);
        } else {
          if (selectedNodes.value[0] === -1) {
            selectedNodes.value = [newNode, -1];
          } else {
            selectedNodes.value = [selectedNodes.value[0], newNode];
          }
        }
        console.log(selectedNodes.value[0], selectedNodes.value[1]);
      }
    }
    provide("handleNodeSelection", handleNodeSelection);

    function moveOutline(newVal, idx) {
      sliderVals.value[idx] = newVal;
    }
    provide("moveOutline", moveOutline);

    function prepareNewScenario(nProds, nCons) {
      selectedNodes.value = [-1, -1];

      matrixComp.value?.clearMatrix();
      chartsComp.value?.clearCharts();

      numberConsumers = nCons;
      numberProducers = nProds;

      const initializeNDarray = (nProds) => {
        return nProds === 0
          ? { matrixData: null, chartsData: null }
          : Array.from({ length: 6 }, () => initializeNDarray(nProds - 1));
      };

      prodCapacities.value = Array.from({ length: nProds }, () => 0);
      dataValues.value = initializeNDarray(nProds);
    }

    provide("prepareNewScenario", prepareNewScenario);

    return {
      handleSimulationData,
      matrixTheme,
      sliderVals,
      matrixData,
      chartsData,
      currTheme,
      handleNodeSelection,
      first,
    };
  },
  components: {
    Sliders,
    Chart,
    Playfield,
    Matrix,
    Charts,
    Drawerbox,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
