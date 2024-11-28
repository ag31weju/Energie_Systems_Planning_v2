<template>
  <Panel id="sliders" header="Sliders">
    <Slider v-model="sliderVal" class="w-56"></Slider>
    {{ sliderVal }}
    <Slider v-model="sliderVal2" class="w-56"></Slider>
    {{ sliderVal2 }}
  </Panel>
</template>

<script>
import Slider from "primevue/slider";
import Panel from "primevue/panel";

export default {
  data() {
    return {
      sliderVal: 0,
      sliderVal2: 100,
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
