/** * App.vue contains all the pages and sets the routes which are set in
main.js * Home.vue is loaded as root and /scenario loads the Scenario creator
page * All routes are set in main.js and vue pages are in frontend\src\views
folder */

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { ref, provide } from "vue";
import Chart from "primevue/chart";
import { usedLanguage } from "./assets/stores/pageSettings";

export default {
  setup() {
    const usedLang = usedLanguage();
    // Initial setting of values
    provide("capacity", usedLang.capacity);
    provide("cost", usedLang.cost);
    provide("battery", usedLang.battery);
    provide("pv", usedLang.pv);
    provide("pv_production", usedLang.pv_production);
    provide("pv_curtailment", usedLang.pv_curtailment);
    provide("demand", usedLang.demand);
    provide("purchased_power", usedLang.purchased_power);
    provide("storage_charge", usedLang.storage_charge);
    provide("storage_discharge", usedLang.storage_discharge);
    provide("storage_level", usedLang.storage_level);
    provide("simulate", usedLang.simulate);
    provide("reset_text", usedLang.reset_text);
    provide("auto", usedLang.auto);
    provide("title_upper_plot", usedLang.title_upper_plot);
    provide("title_middle_plot", usedLang.title_middle_plot);
    provide("title_lower_plot", usedLang.title_lower_plot);
    provide("load_scenario", usedLang.load_scenario);
    provide("upload_scenario", usedLang.upload_scenario);
    provide("toggle_grid", usedLang.toggle_grid);
    provide("add_consumer", usedLang.add_consumer);
    provide("add_energy_source", usedLang.add_energy_source);
    provide("clear_nodes", usedLang.clear_nodes);
    provide("save_text", usedLang.save_text);
    provide("lock_text", usedLang.lock_text);
    provide("unlock_text", usedLang.unlock_text);
    provide("add_edge", usedLang.add_edge);
    provide("upload_json", usedLang.upload_json);
    return {};
  },
  components: {
    Chart,
  },
};
</script>
