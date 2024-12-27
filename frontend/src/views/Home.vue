<template>
  <div id="drawerbox">
    <Drawerbox
      @changeLanguage="updateLanguage"
      @changeMatrixTheme="updateMatrixTheme"
    ></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield
          v-bind:load_scenario="load_scenario"
          v-bind:upload_scenario="upload_scenario"
          v-bind:toggle_grid="toggle_grid"
          v-bind:add_consumer="add_consumer"
          v-bind:add_energy_source="add_energy_source"
          v-bind:clear_nodes="clear_nodes"
        ></Playfield>
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
        <Matrix
          :matrixData="matrixData"
          :matrixTheme="matrixTheme"
          :sliderVals="sliderVals"
        ></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts :chartsData="chartsData"></Charts>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { provide, ref } from "vue";
import Chart from "primevue/chart";
import Sliders from "../components/Sliders.vue";
import Playfield from "../components/PlayfieldStudent.vue";
import Matrix from "../components/Matrix.vue";
import Charts from "../components/Charts.vue";
import Drawerbox from "../components/Drawerbox.vue";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  data() {
    return {
      sliderVals: undefined,
      matrixData: undefined,
      chartsData: undefined,
      isAutoSimulating: false,
      stopAutoSimulate: false,
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
    let upload_scenario = ref(currentLangJSON.upload_scenario);
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
      upload_scenario.value = currentLangJSON.upload_scenario;
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
      upload_scenario,
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
      this.matrixTheme = darkMode
        ? { backgroundColor: "rgb(39, 39, 39)", gridColor: "white" }
        : { backgroundColor: "white", gridColor: "black" };
    },
    async fetchMessage() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/");
        this.message = response.data.message;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
    handleSimulationData(propagateChange) {
      if (propagateChange.reset) {
        this.isAutoSimulating = false;
        this.stopAutoSimulate = true;
      }
      if (!this.isAutoSimulating) {
        if (propagateChange.autoSimulate) {
          this.isAutoSimulating = true;
          this.autoSimulateData(propagateChange);
        } else {
          const currentSliderVals = propagateChange.sliderVals.map((el) => {
            return el.value;
          });
          this.simulateData(propagateChange, currentSliderVals);
        }
      }
    },
    async autoSimulateData(propagateChange) {
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      for (let rowIndex = 0; rowIndex < 6; rowIndex++) {
        for (let colIndex = 0; colIndex < 6; colIndex++) {
          if (this.stopAutoSimulate) {
            this.stopAutoSimulate = false;
            return;
          }
          let currentSliderVals = [colIndex, rowIndex];
          this.simulateData(propagateChange, currentSliderVals);
          await sleep(700);
        }
      }
      this.isAutoSimulating = false;
    },
    simulateData(propagateChange, currentSliderVals) {
      const newValues =
        propagateChange.simData[currentSliderVals[1]][currentSliderVals[0]];
      this.sliderVals = currentSliderVals;
      this.matrixData = {
        reset: propagateChange.reset,
        matrixValue: newValues.matrixData,
      };
      this.chartsData = newValues.chartsData;
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
