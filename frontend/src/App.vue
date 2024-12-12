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
        <Matrix :matrixData="matrixData"></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts :chartsData="chartsData"></Charts>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "primevue/chart";
import Sliders from "./components/Sliders.vue";
import Playfield from "./components/Playfield.vue";
import Matrix from "./components/Matrix.vue";
import Charts from "./components/Charts.vue";
import Drawerbox from "./components/Drawerbox.vue";

export default {
  data() {
    return {
      matrixData: undefined,
      chartsData: undefined,
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
  methods: {
    async fetchMessage() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/");
        this.message = response.data.message;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    handleSimulationData(simData) {
      this.matrixData = simData.matrixData;
      this.chartsData = simData.chartsData;
    },
  },
};
</script>

<style>
@import "./assets/main.css";
</style>
