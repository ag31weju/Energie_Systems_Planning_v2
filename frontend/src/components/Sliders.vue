<template>
    <Slider v-model="sliderVal" class="w-56"></Slider>
    {{ sliderVal }}
    <Slider v-model="sliderVal2" class="w-56"></Slider>
    {{ sliderVal2 }}
</template>

<script>
import Slider from "primevue/slider";

export default {
  data() {
    return {
      sliderVal: 0,
      sliderVal2: 100,
    };
  },
  components: {
    Slider,
  },
  methods: {},
};
</script>

<style>
@import "../assets/main.css";
</style>
