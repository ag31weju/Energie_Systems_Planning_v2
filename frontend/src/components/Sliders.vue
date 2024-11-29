<template>
  <Panel id="sliders" header="Sliders">
    <Slider
      v-model="sliderVal"
      :min="0"
      :max="5"
      :step="step"
      class="w-56"
    ></Slider>
    {{ sliderVal / step }}
    <Slider
      v-model="sliderVal2"
      :min="0"
      :max="5"
      :step="step"
      class="w-56"
    ></Slider>
    {{ sliderVal2 / step }}
    <div id="slider-buttons-container">
      <button @click="reset" class="slider-button">Reset</button>
      <button @click="autoSimulate" class="slider-button">Auto Simulate</button>
      <button @click="simulate" class="slider-button">Simulate</button>
    </div>
  </Panel>
</template>

<script>
import Slider from "primevue/slider";
import Panel from "primevue/panel";

export default {
  data() {
    return {
      step: 1,
      sliderVal: 0,
      sliderVal2: 5,
    };
  },
  components: {
    Slider,
    Panel,
  },
  methods: {},
};
</script>

<style>
@import "../assets/main.css";
</style>
