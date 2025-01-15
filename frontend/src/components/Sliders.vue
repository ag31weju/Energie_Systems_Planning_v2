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
      <Button
        @click="reset"
        class="button"
        v-bind:label="usedLang.reset_text"
      ></Button>
      <Button
        @click="autoSimulateRequest"
        class="button"
        v-bind:label="usedLang.auto"
      >
      </Button>
      <Button
        @click="simulateRequest"
        class="button"
        v-bind:label="usedLang.simulate"
      ></Button>
    </div>
  </Panel>
</template>

<script>
import Slider from "primevue/slider";
import Button from "primevue/button";
import Panel from "primevue/panel";
import axios from "axios";
import { ref, watch, onMounted, inject } from "vue";
import { usedLanguage } from "../assets/stores/pageSettings";

export default {
  props: ["auto", "simulate", "reset_text"],
  setup(props, context) {
    const usedLang = usedLanguage();

    let selectedNodes = inject("selectedNodes");

    const step = ref(1);
    const sliderList = ref([]);

    async function reset() {
      sliderList.value.forEach((slider) => (slider.value = 0));
      // Send reset flag to the backend
      const url = "http://127.0.0.1:8000/api/save-slider-data/";
      const sliderData = {
        autoSimulate: false,
        reset: true, // Flag to indicate reset action to reset graphs and matrix
        sliders: sliderList.value.map((slider) => ({
          type: slider.type,
          value: slider.value,
        })),
      };
      await postAndGet(url, sliderData);
    }
    async function simulateRequest() {
      const url = "http://127.0.0.1:8000/api/save-slider-data/";
      const sliderData = {
        autoSimulate: false,
        reset: false,
        sliders: sliderList.value.map((slider) => ({
          type: slider.type,
          value: slider.value,
        })),
      };

      // Send the full slider data to the backend
      await postAndGet(url, sliderData);
    }

    async function autoSimulateRequest() {
      const url = "http://127.0.0.1:8000/api/save-slider-data/";
      const sliderData = {
        reset: false,
        autoSimulate: true, // Send the boolean flag for auto simulation
        sliders: sliderList.value.map((slider) => ({
          type: slider.type,
          value: slider.value,
        })),
      };

      // Send the auto-simulation request with the flag
      await postAndGet(url, sliderData);
    }

    async function postAndGet(url, data) {
      try {
        const autoSimulate = data.autoSimulate;
        const reset = data.reset;
        const sliderVals = data.sliders;

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

        const propagateChange = {
          simData: simData.mainData,
          reset: reset,
          autoSimulate: autoSimulate,
          sliderVals: sliderVals,
          bestIdx: simData.bestIdx,
        };
        context.emit("getSimulationData", propagateChange);
      } catch (error) {
        console.error("Error sending data to backend:", error);
        throw error; // Re-throw the error to handle it in the calling method
      }
    }

    function changeSliders(newVal) {
      sliderList.value = [
        { value: 0, nodeID: selectedNodes.value[0] },
        { value: 0, nodeID: selectedNodes.value[1] },
      ];
    }

    onMounted(() => {
      sliderList.value = [
        { value: 0, nodeID: selectedNodes.value[0] },
        { value: 0, nodeID: selectedNodes.value[1] },
      ];
    });

    watch(
      () => selectedNodes.value,
      (newVal) => changeSliders(newVal),
      {
        deep: true,
      }
    );

    return {
      usedLang,
      sliderList,
      step,
      reset,
      autoSimulateRequest,
      simulateRequest,
    };
  },
  components: {
    Slider,
    Panel,
    Button,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
