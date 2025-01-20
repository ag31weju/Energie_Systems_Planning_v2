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
        @click="postAndGet(true, false, 'reset')"
        class="button"
        v-bind:label="usedLang.reset_text"
      ></Button>
      <Button
        @click="postAndGet(false, true, 'auto')"
        class="button"
        v-bind:label="usedLang.auto"
      >
      </Button>
      <Button
        @click="postAndGet(false, false, 'simulate')"
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
    const url = "http://127.0.0.1:8000/api/save-slider-data/";

    let selectedNodes = inject("selectedNodes");
    let moveOutline = inject("moveOutline");
    let isAutoSimulating = inject("isAutoSimulating");
    let prodCapacities = inject("prodCapacities");

    const step = ref(1);
    const sliderList = ref([]);

    async function postAndGet(reset, autoSimulate, test) {
      console.log(test);
      try {
        const autoSimulate = props.autoSimulate;
        const reset = props.reset;

        const data = {
          reset: reset,
          autoSimulate: autoSimulate, // Send the boolean flag for auto simulation
          prodCapacities: prodCapacities.value,
        };

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

        console.log(sliderVals);
        const propagateChange = {
          simData: simData.mainData,
          reset: reset,
          autoSimulate: autoSimulate,
          sliderVals: sliderVals,
          bestIdx: simData.bestIdx,
        };
        //  context.emit("getSimulationData", propagateChange);
      } catch (error) {
        console.error("Error sending data to backend:", error);
        throw error; // Re-throw the error to handle it in the calling method
      }
    }

    function startMoveOutline(event, index) {
      if (!isAutoSimulating.value) moveOutline(event, index);
    }

    function changeSliders(newVal) {
      sliderList.value.forEach((slider, idx) => {
        slider.nodeID = newVal[idx];
      });
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
