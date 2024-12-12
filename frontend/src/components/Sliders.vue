<template>
  <Panel id="sliders" header="Sliders">
    <div v-for="(_, index) in sliderList" :key="index">
      <Slider
        v-model="sliderList[index].value"
        :min="0"
        :max="5"
        :step="step"
        class="w-56"
        style="margin: 10px"
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
    async reset() {
      this.sliderList.forEach((slider) => (slider.value = 0));
      // Send reset flag to the backend
      const url = "http://127.0.0.1:8000/api/save-slider-data/";
      const sliderData = {
        autoSimulate: false,
        reset: true, // Flag to indicate reset action to reset graphs and matrix
        sliders: this.sliderList.map((slider) => ({
          type: slider.type,
          value: slider.value,
        })),
      };
      await this.postAndGet(url, sliderData);
    },
    async simulateRequest() {
      const url = "http://127.0.0.1:8000/api/save-slider-data/";
      const sliderData = {
        autoSimulate: false,
        reset: false,
        sliders: this.sliderList.map((slider) => ({
          type: slider.type,
          value: slider.value,
        })),
      };

      // Send the full slider data to the backend
      await this.postAndGet(url, sliderData);
    },

    async autoSimulateRequest() {
      const url = "http://127.0.0.1:8000/api/save-slider-data/";
      const sliderData = {
        reset: false,
        autoSimulate: true, // Send the boolean flag for auto simulation
        sliders: this.sliderList.map((slider) => ({
          type: slider.type,
          value: slider.value,
        })),
      };

      // Send the auto-simulation request with the flag
      await this.postAndGet(url, sliderData);
    },
    async postAndGet(url, data) {
      try {
        const response = await axios
          .post(url, data, {
            headers: {
              "Content-Type": "application/json", // Ensures JSON format
            },
          })
          .catch((e) => console.error("POST did not work", e));
        //if response is ok, then do GET function
        const simData = await axios
          .get(/* url for receiving data */)
          .then((res) => {
            return res.data;
          })
          .catch((e) => console.error("GET did not work:", e));

        /* Destructure simData into multiple parts
         */
        const tempData = {
          matrixData: Array.from({ length: 6 }, () =>
            Array.from({ length: 6 }, () => Math.floor(Math.random() * 100))
          ),
          chartsData: {
            lineChartData: Array.from(
              { length: 25 },
              (_) => Math.random() * 100
            ),
            barChartData: {
              demand: Array.from({ length: 25 }, (_) =>
                Math.floor(Math.random() * -100)
              ),
              produced: Array.from({ length: 25 }, (_) =>
                Math.floor(Math.random() * 100)
              ),
            },
          },
        };
        this.$emit("getSimulationData", tempData);
      } catch (error) {
        console.error("Error sending data to backend:", error);
        throw error; // Re-throw the error to handle it in the calling method
      }
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
