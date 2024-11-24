<template>
  <div id="rootdiv" class="grid-row">
    <div id="language-buttons-container">
      <button @click="setLanguage('en')" id="language-button-en">
        <img src="@/assets/en.png" alt="English Flag" />
      </button>
      <button @click="setLanguage('de')" id="language-button-de">
        <img src="@/assets/de.png" alt="German Flag" />
      </button>
    </div>
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <div id="image"></div>
      </div>
      <div id="inputbox" class="grid-column">
        <div style="min-width: 50%">
          <Slider v-model="sliderVal" class="w-56"></Slider>
          {{ sliderVal }}
          <Slider v-model="sliderVal2" class="w-56"></Slider>
          {{ sliderVal2 }}
        </div>
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
        <div id="chart2-box" style="background-color: blue; margin-top: 20px;">
           <p>Chart 2</p>
            <Chart
             type="line"
            :data="chartset2"
            :options="chartOptions2"
            class="h-[30rem]"/>
        </div>
      </div>
      <div id="checkboxes" class="grid-column">
        <div id="cbrow" class="grid-column">
          <input type="checkbox" id="ibbbfw" />
          <input type="checkbox" id="igod8q" />
          <input type="checkbox" id="ixlfdm" />
        </div>
        <div id="cbrow" class="grid-column">
          <input type="checkbox" id="ikyips" />
          <input type="checkbox" id="i13dy2" />
          <input type="checkbox" id="i00u17" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Slider from "primevue/slider";
import Chart from "primevue/chart";

export default {
  data() {
  return {
    sliderVal: 0,
    sliderVal2: 100,
    // Data for Chart 1
    chartset: {
      labels: ['January', 'February', 'March', 'April', 'May', 'June'],
      datasets: [
        {
          label: 'Graph 1',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1,
          data: [65, 59, 80, 81, 56, 55],
        },
        {
          label: 'Graph 2',
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
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
          position: 'left',
        },
      },
    },
    // Data for Chart 2
    chartset2: {
      labels: ['July', 'August', 'September', 'October', 'November', 'December'],
      datasets: [
        {
          label: 'Graph A',
          backgroundColor: 'rgba(153, 102, 255, 0.2)',
          borderColor: 'rgba(153, 102, 255, 1)',
          borderWidth: 1,
          data: [45, 67, 75, 50, 40, 90],
        },
        {
          label: 'Graph B',
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
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
          position: 'top',
        },
      },
    },
  };
},

  
  components: {
    Slider,
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
