<template>
  <div id="drawerbox">
    <Drawerbox
      @changeLanguage="updateLanguage"
      @changeMatrixTheme="updateMatrixTheme"
    ></Drawerbox>
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
        <Matrix></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts :chartsData="chartsData"></Charts>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import Chart from "primevue/chart";
import Sliders from "../components/Sliders.vue";
import Playfield from "../components/PlayfieldStudent.vue";
import Matrix from "../components/Matrix.vue";
import Charts from "../components/Charts.vue";
import Drawerbox from "../components/Drawerbox.vue";

export default {
  setup() {
    const sliderVals = ref(undefined);
    const matrixData = ref(undefined);
    const chartsData = ref(undefined);
    const isAutoSimulating = ref(false);
    const stopAutoSimulate = ref(false);

    const matrixTheme = ref({ backgroundColor: "white", gridColor: "black" });

    function updateMatrixTheme(darkMode) {
      matrixTheme.value = darkMode
        ? { backgroundColor: "rgb(39, 39, 39)", gridColor: "white" }
        : { backgroundColor: "white", gridColor: "black" };
    }

    function handleSimulationData(propagateChange) {
      if (propagateChange.reset) {
        isAutoSimulating.value = false;
        stopAutoSimulate.value = true;
      }
      if (!isAutoSimulating.value) {
        if (propagateChange.autoSimulate) {
          isAutoSimulating.value = true;
          autoSimulateData(propagateChange);
        } else {
          const currentSliderVals = propagateChange.sliderVals.map((el) => {
            return el.value;
          });
          simulateData(propagateChange, currentSliderVals);
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
          let currentSliderVals = [colIndex, rowIndex];
          simulateData(propagateChange, currentSliderVals);
          await sleep(700);
        }
      }
      isAutoSimulating.value = false;
    }
    function simulateData(propagateChange, currentSliderVals) {
      const newValues =
        propagateChange.simData[currentSliderVals[1]][currentSliderVals[0]];
      sliderVals.value = currentSliderVals;
      matrixData.value = {
        reset: propagateChange.reset,
        matrixValue: newValues.matrixData,
      };
      chartsData.value = newValues.chartsData;
    }

    return {
      updateMatrixTheme,
      handleSimulationData,
      matrixTheme,
      sliderVals,
      matrixData,
      chartsData,
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
