/**
* App.vue contains all the pages and sets the routes which are set in main.js
* Home.vue is loaded as root and /scenario loads the Scenario creator page
* All routes are set in main.js and vue pages are in frontend\src\views folder
*/

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";
import Chart from "primevue/chart";
import Sliders from "./components/Sliders.vue";
import Playfield from "./components/Playfield.vue";
import Matrix from "./components/Matrix.vue";
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
    let toggle_grid = ref(currentLangJSON.toggle_grid);
    let add_consumer = ref(currentLangJSON.add_consumer);
    let add_energy_source = ref(currentLangJSON.add_energy_source);
    let clear_nodes = ref(currentLangJSON.clear_nodes);

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

      capacity.value = currentLangJSON.capacity;
      cost.value = currentLangJSON.cost;
      battery.value = currentLangJSON.battery;
      pv.value = currentLangJSON.pv;
      pv_production.value = currentLangJSON.pv_production;
      pv_curtailment.value = currentLangJSON.pv_curtailment;
      demand.value = currentLangJSON.demand;
      purchased_power.value = currentLangJSON.purchased_power;
      storage_charge.value = currentLangJSON.storage_charge;
      storage_discharge.value = currentLangJSON.storage_discharge;
      storage_level.value = currentLangJSON.storage_level;
      simulate.value = currentLangJSON.simulate;
      reset_text.value = currentLangJSON.reset_text;
      auto.value = currentLangJSON.auto;
      title_upper_plot.value = currentLangJSON.title_upper_plot;
      title_middle_plot.value = currentLangJSON.title_middle_plot;
      title_lower_plot.value = currentLangJSON.title_lower_plot;
      load_scenario.value = currentLangJSON.load_scenario;
      toggle_grid.value = currentLangJSON.toggle_grid;
      add_consumer.value = currentLangJSON.add_consumer;
      add_energy_source.value = currentLangJSON.add_energy_source;
      clear_nodes.value = currentLangJSON.clear_nodes;
    }

    const matrixTheme = ref("white");
    return {
      updateLanguage,
      matrixTheme,
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
      toggle_grid,
      add_consumer,
      add_energy_source,
      clear_nodes,
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
    updateMatrixTheme(darkMode) {
      this.matrixTheme = darkMode ? "rgb(39, 39, 39)" : "white";
    },
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
