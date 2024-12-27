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
        <Playfield></Playfield>
      </div>
      <div id="slider-box">
        <Sliders @getSimulationData="handleSimulationData"></Sliders>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="matrix-box" class="grid-column">
        <Matrix></Matrix>
      </div>
      <div id="charts-box" class="grid-column">
        <Charts :chartsData="chartsData"></Charts>
      </div>
    </div>
  </div>
</template>

<script>
import { provide, ref } from "vue";
import Chart from "primevue/chart";
import Sliders from "../components/Sliders.vue";
import Playfield from "../components/PlayfieldStudent.vue";
import Matrix from "../components/Matrix.vue";
import Charts from "../components/Charts.vue";
import Drawerbox from "../components/Drawerbox.vue";

export default {
  setup() {
    const sliderVals = ref(undefined);
    const matrixData = ref(undefined);
    const chartsData = ref(undefined);
    const isAutoSimulating = ref(false);
    const stopAutoSimulate = ref(false);

    const matrixTheme = ref({ backgroundColor: "white", gridColor: "black" });

    function updateMatrixTheme(darkMode) {
      matrixTheme.value = darkMode
        ? { backgroundColor: "rgb(39, 39, 39)", gridColor: "white" }
        : { backgroundColor: "white", gridColor: "black" };
    }

    function handleSimulationData(propagateChange) {
      if (propagateChange.reset) {
        isAutoSimulating.value = false;
        stopAutoSimulate.value = true;
      }
      if (!isAutoSimulating.value) {
        if (propagateChange.autoSimulate) {
          isAutoSimulating.value = true;
          autoSimulateData(propagateChange);
        } else {
          const currentSliderVals = propagateChange.sliderVals.map((el) => {
            return el.value;
          });
          simulateData(propagateChange, currentSliderVals);
        }
      }
    }
    async function autoSimulateData(propagateChange) {
      const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
      for (let rowIndex = 0; rowIndex < 6; rowIndex++) {
        for (let colIndex = 0; colIndex < 6; colIndex++) {
          if (stopAutoSimulate.value) {
            stopAutoSimulate.value = false;
            return;
          }
          let currentSliderVals = [colIndex, rowIndex];
          simulateData(propagateChange, currentSliderVals);
          await sleep(700);
        }
      }
      isAutoSimulating.value = false;
    }
    function simulateData(propagateChange, currentSliderVals) {
      const newValues =
        propagateChange.simData[currentSliderVals[1]][currentSliderVals[0]];
      sliderVals.value = currentSliderVals;
      matrixData.value = {
        reset: propagateChange.reset,
        matrixValue: newValues.matrixData,
      };
      chartsData.value = newValues.chartsData;
    }

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
};
</script>

<style>
@import "../assets/main.css";
</style>
