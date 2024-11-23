<template>
  <div id="rootdiv" class="grid-row">
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
