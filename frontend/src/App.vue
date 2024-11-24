<template>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <div id="image"></div>
      </div>
      <div id="inputbox" class="grid-column">
          <Sliders></Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix" class="grid-column">
        <label>Matrix<br /></label>
      </div>
      <div id="charts" class="grid-column">
        <label>Charts</label>
        <div id="chart1-box" style="background-color: red">
          <p>Hello</p>
          <Chart
            type="bar"
            :data="chartset"
            :options="chartOptions"
            class="h-[30rem]"
          />
        </div>
      </div>
      <Checkboxes></Checkboxes>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "primevue/chart";
import Sliders from "./components/Sliders.vue";
import Checkboxes from "./components/Checkboxes.vue";

export default {
  data() {
    return {
      
    };
  },
  components: {
    Checkboxes,
    Sliders,
    Chart,
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
  },
};
</script>

<style>
@import "./assets/main.css";
</style>
