<template>
  <div id="drawerbox">
    <Drawerbox @changeLanguage="updateLanguage"></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield v-bind:load_scenario="load_scenario"></Playfield>
      </div>
      <div id="slider-box">
        <Sliders
          v-bind:reset_text="reset_text"
          v-bind:simulate="simulate"
          v-bind:auto="auto"
          @getSimulationData="handleSimulationData"
        ></Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix-box" class="grid-column">
        <Matrix :matrixData="matrixData"></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts :chartsData="chartsData"></Charts>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import Chart from "primevue/chart";
import Sliders from "./components/Sliders.vue";
import Playfield from "./components/Playfield.vue";
import Matrix from "./components/MatrixOLD2.vue";
import Charts from "./components/Charts.vue";
import Drawerbox from "./components/Drawerbox.vue";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  data() {
    return {
      matrixData: undefined,
      chartsData: undefined,
    };
  },
  setup() {
    const currentLang = ref("EN");
    let currentLangJSON = ENLang;
    let capacity = ref(currentLangJSON.capacity);
    let cost = ref(currentLangJSON.cost);
    let battery = ref(currentLangJSON.battery);
    let pv = ref(currentLangJSON.pv);
    let pv_production = ref(currentLangJSON.pv_production);
    let pv_curtailment = ref(currentLangJSON.pv_curtailment);
    let demand = ref(currentLangJSON.demand);
    let purchased_power = ref(currentLangJSON.purchased_power);
    let storage_charge = ref(currentLangJSON.storage_charge);
    let storage_discharge = ref(currentLangJSON.storage_discharge);
    let storage_level = ref(currentLangJSON.storage_level);
    let simulate = ref(currentLangJSON.simulate);
    let reset_text = ref(currentLangJSON.reset_text);
    let auto = ref(currentLangJSON.auto);
    let title_upper_plot = ref(currentLangJSON.title_upper_plot);
    let title_middle_plot = ref(currentLangJSON.title_middle_plot);
    let title_lower_plot = ref(currentLangJSON.title_lower_plot);
    let load_scenario = ref(currentLangJSON.load_scenario);

    function updateLanguage(language) {
      if (currentLang.value == language) {
        return;
      }

      if (language == "EN") {
        currentLangJSON = ENLang;
        currentLang.value = "EN";
      }

      if (language == "DE") {
        currentLangJSON = DELang;
        currentLang.value = "DE";
      }

      capacity.value = ref(currentLangJSON.capacity);
      cost.value = ref(currentLangJSON.cost);
      battery.value = ref(currentLangJSON.battery);
      pv.value = ref(currentLangJSON.pv);
      pv_production.value = ref(currentLangJSON.pv_production);
      pv_curtailment.value = ref(currentLangJSON.pv_curtailment);
      demand.value = ref(currentLangJSON.demand);
      purchased_power.value = ref(currentLangJSON.purchased_power);
      storage_charge.value = ref(currentLangJSON.storage_charge);
      storage_discharge.value = ref(currentLangJSON.storage_discharge);
      storage_level.value = ref(currentLangJSON.storage_level);
      simulate.value = ref(currentLangJSON.simulate);
      reset_text.value = ref(currentLangJSON.reset_text);
      auto.value = ref(currentLangJSON.auto);
      title_upper_plot.value = ref(currentLangJSON.title_upper_plot);
      title_middle_plot.value = ref(currentLangJSON.title_middle_plot);
      title_lower_plot.value = ref(currentLangJSON.title_lower_plot);
      load_scenario.value = ref(currentLangJSON.load_scenario);
    }

    return {
      updateLanguage,
      capacity,
      cost,
      battery,
      pv,
      pv_production,
      pv_curtailment,
      demand,
      purchased_power,
      storage_charge,
      storage_discharge,
      storage_level,
      simulate,
      reset_text,
      auto,
      title_upper_plot,
      title_middle_plot,
      title_lower_plot,
      load_scenario,
    };
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
    handleSimulationData(simData) {
      this.matrixData = simData.matrixData;
      this.chartsData = simData.chartsData;
    },
  },
};
</script>

<style>
@import "./assets/main.css";
</style>
