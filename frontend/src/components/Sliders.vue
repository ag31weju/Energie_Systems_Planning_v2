<template>
  <Panel id="sliders">
    <div id="sliders-grid">
      <div
        id="slider-sliders-container"
        v-for="(_, index) in sliderList"
        :key="index"
      >
        <Slider
          v-model="sliderList[index].value"
          :min="0"
          :max="5"
          :step="step"
          class="w-56"
        ></Slider>
        {{ sliderList[index].value / step }}
      </div>
      <div id="slider-buttons-container">
        <button @click="reset" class="slider-button">Reset</button>
        <button @click="autoSimulateRequest" class="slider-button">
          Auto Simulate
        </button>
        <button @click="simulateRequest" class="slider-button">Simulate</button>
      </div>
    </div>
  </Panel>
</template>

<script>
import Slider from "primevue/slider";
import Panel from "primevue/panel";
import axios from "axios";

export default {
  data() {
    return {
      propData: ["test1", "test2"], //This array tells what the amount and type of nodes are inside the graph
      step: 1,
      sliderList: [],
      sliderVal: 0,
      sliderVal2: 5,
    };
  },
  components: {
    Slider,
    Panel,
  },
  mounted() {
    this.sliderList = Array.from(
      { length: this.propData.length },
      (_, index) => {
        return {
          value: 0,
          type: this.propData[index],
        };
      }
    );
  },
  methods: {
    reset() {},
    async simulateRequest() {
      const url = "someserverendpoint";
      const data = {
        sliderList: this.sliderList,
        reqType: "once",
      };
      await this.sendRequest(url, data);
    },
    async autoSimulateRequest() {
      const url = "someserverendpoint";
      const data = {
        sliderList: this.sliderList,
        reqType: "all",
      };
      await this.sendRequest(url, data);
    },
    async sendRequest(url, data) {
      try {
        const response = await axios.post(url, data);
        console.log("Response:", response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
