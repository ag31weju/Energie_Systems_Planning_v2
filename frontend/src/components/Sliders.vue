<template>
  <Panel id="sliders" header="Sliders">
    <div v-for="(_, index) in sliderList" :key="index">
      <Slider
        v-model="sliderList[index].value"
        :min="0"
        :max="5"
        :step="step"
        :disabled="isAutoSimulating || sliderList[index].nodeID === -1"
        class="w-56"
        :id="`slider${index}`"
        @change="(event) => startMoveOutline(event, index)"
        style="margin: 10px"
      ></Slider>
      {{ sliderList[index].value / step }}
    </div>

    <div id="slider-buttons-container">
      <Button
        @click="postAndGet(true, false)"
        class="button"
        v-bind:label="usedLang.reset_text"
        :disabled="sliderList.some((node) => node.nodeID === -1)"
      ></Button>
      <Button
        @click="postAndGet(false, true)"
        class="button"
        v-bind:label="usedLang.auto"
        :disabled="
          isAutoSimulating || sliderList.some((node) => node.nodeID === -1)
        "
      >
      </Button>
      <Button
        @click="postAndGet(false, false)"
        class="button"
        v-bind:label="usedLang.simulate"
        :disabled="
          isAutoSimulating || sliderList.some((node) => node.nodeID === -1)
        "
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
import { useDataStore } from "../assets/stores/dataValues";
import { useScenarioStore } from "../assets/stores/scenarioStore";

export default {
  props: ["auto", "simulate", "reset_text"],
  setup(props, context) {
    const usedLang = usedLanguage();
    const dataStore = useDataStore();
    const url = "http://127.0.0.1:8000/api/save-slider-data/";
    const scenarioStore = useScenarioStore();

    let moveOutline = inject("moveOutline");
    let isAutoSimulating = inject("isAutoSimulating");

    const step = ref(1);
    const sliderList = ref([
      { value: 0, nodeID: -1 },
      { value: 0, nodeID: -1 },
    ]);

    async function postAndGet(reset, autoSimulate) {
      sliderList.value.forEach((slider) => {
        dataStore.prodCapacities.set(slider.nodeID, slider.value);
      });
      try {
        const data = {
          nodes: scenarioStore.nodes, 
          edges: scenarioStore.edges,
          sliderData:{
          reset: reset,
          autoSimulate: autoSimulate, // Send the boolean flag for auto simulation
          prodCapacities: Array.from(dataStore.prodCapacities),
        }};

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

        const sliderVals = sliderList.value.map((slider) => {
          return slider.value;
        });

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

    function startMoveOutline(event, index) {
      if (!isAutoSimulating.value) {
        moveOutline(event, index);
      }
    }

    function changeSliders(newVal) {
      sliderList.value.forEach((slider, idx) => {
        slider.nodeID = newVal[idx];
        slider.value = dataStore.prodCapacities.has(
          dataStore.selectedNodes[idx]
        )
          ? dataStore.prodCapacities.get(dataStore.selectedNodes[idx])
          : 0;
      });
    }

    watch(
      () => dataStore.selectedNodes,
      (newVal) => changeSliders(newVal),
      {
        deep: true,
      }
    );

    return {
      usedLang,
      sliderList,
      step,
      postAndGet,
      startMoveOutline,
      isAutoSimulating,
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
