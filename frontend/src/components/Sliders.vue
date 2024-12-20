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
      <Button @click="reset" class="button" v-bind:label="reset_text"></Button>
      <Button @click="autoSimulateRequest" class="button" v-bind:label="auto">
      </Button>
      <Button
        @click="simulateRequest"
        class="button"
        v-bind:label="simulate"
      ></Button>
    </div>
  </Panel>
</template>

<script>
import Slider from "primevue/slider";
import Button from "primevue/button";
import Panel from "primevue/panel";
import axios from "axios";

export default {
  props: ["auto", "simulate", "reset_text"],
  data() {
    return {
      propData: ["test1", "test2"], //This array tells what the amount and type of nodes are inside the graph
      step: 1,
      sliderList: [],
    };
  },
  components: {
    Slider,
    Panel,
    Button,
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
          .get(url)
          .then((res) => {
            return res.data;
          })
          .catch((e) => console.error("GET did not work:", e));
        this.$emit("getSimulationData", simData);
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
