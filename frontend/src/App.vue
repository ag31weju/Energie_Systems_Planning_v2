<template>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <div id="image"></div>
        <Playfield></Playfield>
      </div>
      <div id="inputbox" class="grid-column">
        <Panel header="Checkboxes">
          <Sliders></Sliders>
        </Panel>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix" class="grid-column">
        <Panel header="Matrix"> </Panel>
      </div>
      <div id="charts" class="grid-column">
        <Panel header="Charts"> </Panel>
      </div>
      <Panel header="Checkboxes">
        <Checkboxes></Checkboxes>
      </Panel>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Chart from "primevue/chart";
import Sliders from "./components/Sliders.vue";
import Checkboxes from "./components/Checkboxes.vue";
import Playfield from "./components/Playfield.vue";
import Panel from "primevue/panel";

export default {
  data() {
    return {};
  },
  components: {
    Checkboxes,
    Sliders,
    Chart,
    Playfield,
    Panel,
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
