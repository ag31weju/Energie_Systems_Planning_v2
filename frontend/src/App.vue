<template>
  <div id="rootdiv" class="grid-row">
    <div id="language-buttons-container">
      <button
        title="Translate to English"
        @click="setLanguage('en')"
        id="language-button-en"
      >
        <img src="@/assets/en.png" alt="English Flag" />
      </button>
      <button
        title="ins Deutsch übersetzen"
        @click="setLanguage('de')"
        id="language-button-de"
      >
        <img src="@/assets/de.png" alt="German Flag" />
      </button>
    </div>
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield></Playfield>
      </div>
      <div id="slider-box">
        <Sliders></Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix-box" class="grid-column">
        <Matrix></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts></Charts>
      </div>
    </div>
  </div>
  <div
      id="drawer-box"
      style="
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
      "
    >
      <Drawerbox></Drawerbox>
    </div>
</template>

<script>
import axios from "axios";
import Chart from "primevue/chart";
import Sliders from "./components/Sliders.vue";
import Playfield from "./components/Playfield.vue";
import Matrix from "./components/Matrix.vue";
import Charts from "./components/Charts.vue";
import Drawerbox from "./components/Drawerbox.vue";

export default {
  data() {
    return {};
  },

  components: {
    Sliders,
    Chart,
    Playfield,
    Matrix,
    Charts,
    Drawerbox,
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
