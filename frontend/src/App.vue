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
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  setup() {
    const currentLang = ref("EN");
    let currentLangJSON = ENLang;

    // Initial setting of values
    provide("capacity", currentLangJSON.capacity);
    provide("cost", currentLangJSON.cost);
    provide("battery", currentLangJSON.battery);
    provide("pv", currentLangJSON.pv);
    provide("pv_production", currentLangJSON.pv_production);
    provide("pv_curtailment", currentLangJSON.pv_curtailment);
    provide("demand", currentLangJSON.demand);
    provide("purchased_power", currentLangJSON.purchased_power);
    provide("storage_charge", currentLangJSON.storage_charge);
    provide("storage_discharge", currentLangJSON.storage_discharge);
    provide("storage_level", currentLangJSON.storage_level);
    provide("simulate", currentLangJSON.simulate);
    provide("reset_text", currentLangJSON.reset_text);
    provide("auto", currentLangJSON.auto);
    provide("title_upper_plot", currentLangJSON.title_upper_plot);
    provide("title_middle_plot", currentLangJSON.title_middle_plot);
    provide("title_lower_plot", currentLangJSON.title_lower_plot);
    provide("load_scenario", currentLangJSON.load_scenario);
    provide("upload_scenario", currentLangJSON.upload_scenario);
    provide("toggle_grid", currentLangJSON.toggle_grid);
    provide("add_consumer", currentLangJSON.add_consumer);
    provide("add_energy_source", currentLangJSON.add_energy_source);
    provide("clear_nodes", currentLangJSON.clear_nodes);
    provide("save_text", currentLangJSON.save_text);
    provide("lock_text", currentLangJSON.lock_text);
    provide("unlock_text", currentLangJSON.unlock_text);
    provide("add_edge", currentLangJSON.add_edge);

    // Updates displayed language
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
      provide("capacity", currentLangJSON.capacity);
      provide("cost", currentLangJSON.cost);
      provide("battery", currentLangJSON.battery);
      provide("pv", currentLangJSON.pv);
      provide("pv_production", currentLangJSON.pv_production);
      provide("pv_curtailment", currentLangJSON.pv_curtailment);
      provide("demand", currentLangJSON.demand);
      provide("purchased_power", currentLangJSON.purchased_power);
      provide("storage_charge", currentLangJSON.storage_charge);
      provide("storage_discharge", currentLangJSON.storage_discharge);
      provide("storage_level", currentLangJSON.storage_level);
      provide("simulate", currentLangJSON.simulate);
      provide("reset_text", currentLangJSON.reset_text);
      provide("auto", currentLangJSON.auto);
      provide("title_upper_plot", currentLangJSON.title_upper_plot);
      provide("title_middle_plot", currentLangJSON.title_middle_plot);
      provide("title_lower_plot", currentLangJSON.title_lower_plot);
      provide("load_scenario", currentLangJSON.load_scenario);
      provide("upload_scenario", currentLangJSON.upload_scenario);
      provide("toggle_grid", currentLangJSON.toggle_grid);
      provide("add_consumer", currentLangJSON.add_consumer);
      provide("add_energy_source", currentLangJSON.add_energy_source);
      provide("clear_nodes", currentLangJSON.clear_nodes);
      provide("save_text", currentLangJSON.save_text);
      provide("lock_text", currentLangJSON.lock_text);
      provide("unlock_text", currentLangJSON.unlock_text);
      provide("add_edge", currentLangJSON.add_edge);
    }

    provide("updageLanguage", updateLanguage(currentLang.value));

    return {
      updateLanguage,
    };
  },
  components: {
    Chart,
  },
};
</script>
