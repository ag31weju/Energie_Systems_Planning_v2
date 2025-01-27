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
import { ref, provide, watch, onMounted, useTemplateRef } from "vue";
import Chart from "primevue/chart";
import Sliders from "../components/Sliders.vue";
import Playfield from "../components/PlayfieldStudent.vue";
import Matrix from "../components/Matrix.vue";
import Charts from "../components/Charts.vue";
import Drawerbox from "../components/Drawerbox.vue";
import { usedTheme } from "../assets/stores/pageSettings";
import { usedDataStore } from "../assets/stores/dataValues";

export default {
  setup(props, context) {
    const first = ref(true);
    const currTheme = usedTheme();

    const dataStore = usedDataStore();
    const selectedNodes = dataStore.selectedNodes;
    const dataValues = dataStore.dataValues;
    const prodCapacities = dataStore.prodCapacities;
    const getDataValuesCell = dataStore.getDataValuesCell;
    const updateDataValuesCell = dataStore.updateDataValuesCell;
    const extractDataValuesCell = dataStore.extractDataValuesCell;

    const sliderVals = ref([0, 0]);
    const matrixData = ref(undefined);
    const chartsData = ref(undefined);

    const isAutoSimulating = ref(false);
    const stopAutoSimulate = ref(false);
    const newScenarioLoaded = ref(false);

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
      if (
        dataStore.selectedNodes[0] === -1 ||
        dataStore.selectedNodes[1] === -1
      )
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
          dataStore.dataValues = propagateChange.simData;
          dataStore.prodCapacities.map(() => 0);
          autoSimulateData(propagateChange);
        } else {
          updateDataValuesCell(dataStore.dataValues, propagateChange);
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
          dataStore.prodCapacities[dataStore.selectedNodes[1]] = rowIndex;
          dataStore.prodCapacities[dataStore.selectedNodes[0]] = colIndex;
          let currentSliderVals = [colIndex, rowIndex];
          let cell = {
            simData: dataStore.getDataValuesCell(propagateChange.simData),
            reset: propagateChange.reset,
            autoSimulate: propagateChange.autoSimulate,
            sliderVals: propagateChange.sliderVals,
            bestIdx: propagateChange.bestIdx,
          };
          simulateData(cell, currentSliderVals);
          await sleep(100);
        }
      }
      sliderVals.value = propagateChange.bestIdx;
      isAutoSimulating.value = false;
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
      console.log(dataStore.dataValues);
    }

    function handleNodeSelection(newNode) {
      if (!isAutoSimulating.value) {
        console.log(selectedNodes);
        //LIFO-wise selection -> 0 first, 1 subsequently
        const idx = dataStore.selectedNodes.findIndex((el) => {
          return el === newNode;
        });
        //if idx >= 0, that means that the node is supposed to be de-highlighted (shifted with idx = 0, popped with idx = 1). Otherwise, it is going to be highlighted (pushed)
        if (idx >= 0) {
          idx === 0
            ? (dataStore.selectedNodes = [dataStore.selectedNodes[1], -1])
            : (dataStore.selectedNodes = [dataStore.selectedNodes[0], -1]);
        } else {
          if (dataStore.selectedNodes[0] === -1) {
            dataStore.selectedNodes = [newNode, -1];
          } else {
            dataStore.selectedNodes = [dataStore.selectedNodes[0], newNode];
          }
        }
        console.log(dataStore.selectedNodes[0], dataStore.selectedNodes[1]);
      }
    }
    provide("handleNodeSelection", handleNodeSelection);

    function moveOutline(newVal, idx) {
      sliderVals.value[idx] = newVal;
    }
    provide("moveOutline", moveOutline);

    //for testing
    onMounted(() => {
      /*
      let prodCapacities = dataStore.prodCapacities;
      dataStore.prodCapacities = "hm";
      prodCapacities = "hm";
      console.log(prodCapacities === dataStore.prodCapacities);
      console.log(prodCapacities);*/
    });

    function prepareNewScenario(nProds, nCons) {
      dataStore.selectedNodes = [-1, -1];

      matrixComp.value?.clearMatrix();
      chartsComp.value?.clearCharts();

      numberConsumers = nCons;
      numberProducers = nProds;

      const initializeNDarray = (nProds) => {
        return nProds === 0
          ? { matrixData: null, chartsData: null }
          : Array.from({ length: 6 }, () => initializeNDarray(nProds - 1));
      };

      dataStore.prodCapacities = Array.from({ length: nProds }, () => 0);
      dataStore.dataValues = initializeNDarray(nProds);

      console.log(dataStore.prodCapacities.length);
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
