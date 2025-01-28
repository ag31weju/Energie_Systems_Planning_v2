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

    const matrixComp = useTemplateRef("matrixComp");
    const chartsComp = useTemplateRef("chartsComp");

    provide("selectedNodes", selectedNodes);
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
      sliderVals.value = propagateChange.bestIdx;
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
      chartsData.value = {
        reset: propagateChange.reset,
        chartsValues: newValues.chartsData,
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

    function clearAll() {
      if (newScenarioLoaded) {
        matrixComp.value?.clearMatrix();
        chartsComp.value?.clearCharts();
        newScenarioLoaded.value = false;
      }
    }

    watch(
      () => newScenarioLoaded,
      (newVal) => clearAll(),
      {
        deep: true,
      }
    );

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
