<template>
  <div id="rootdiv" class="grid-row">
    <div id="language-buttons-container">
      <button title="Translate to English" @click="setLanguage('en')" id="language-button-en">
        <img src="@/assets/en.png" alt="English Flag" />
      </button>
      <button title="ins Deutsch übersetzen" @click="setLanguage('de')" id="language-button-de">
        <img src="@/assets/de.png" alt="German Flag" />
      </button>
    </div>
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield></Playfield>
      </div>
      <div id="slider-box">
          <Sliders></Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix-box" class="grid-column">
          <Matrix></Matrix>
      </div>
      <div id="charts" class="grid-column">
        <Panel header="Charts">
          <div id="chart1-box">
            <Chart
              type="bar"
              :data="chartset"
              :options="chartOptions"
              class="h-[30rem]"
            />
          </div>
          <div id="chart2-box" style="margin-top: 10px">
            <Chart
              type="line"
              :data="chartset2"
              :options="chartOptions2"
              class="h-[30rem]"
            />
          </div>
        </Panel>
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
import Playfield from "./components/Playfield.vue";
import Panel from "primevue/panel";
import Matrix from "./components/Matrix.vue";

export default {
  data() {
    return {
      sliderVal: 0,
      sliderVal2: 100,
      // Data for Chart 1
      chartset: {
        labels: ["January", "February", "March", "April", "May", "June"],
        datasets: [
          {
            label: "Graph 1",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
            data: [65, 59, 80, 81, 56, 55],
          },
          {
            label: "Graph 2",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
            data: [28, 48, 40, 19, 86, 27],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "left",
          },
        },
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          }
        }
      },
      // Data for Chart 2
      chartset2: {
        labels: [
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        datasets: [
          {
            label: "Graph A",
            backgroundColor: "rgba(153, 102, 255, 0.2)",
            borderColor: "rgba(153, 102, 255, 1)",
            borderWidth: 1,
            data: [45, 67, 75, 50, 40, 90],
          },
          {
            label: "Graph B",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            data: [30, 40, 55, 70, 60, 80],
          },
        ],
      },
      chartOptions2: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "top",
          },
        }
      },
    };
  },

  components: {
    Checkboxes,
    Sliders,
    Chart,
    Playfield,
    Panel,
    Matrix,
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
