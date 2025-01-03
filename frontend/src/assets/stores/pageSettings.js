import { defineStore } from "pinia";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export const usedTheme = defineStore("usedTheme", {
  state: () => {
    let themeSymbol = "☀️";
    let currentTheme = "LIGHT";
    let matrixTheme = {
      backgroundColor: "white",
      gridColor: "black",
    };
    let body = document.body;
    return {
      themeSymbol,
      currentTheme,
      body,
      matrixTheme,
    };
  },
  actions: {
    toggleTheme() {
      if (this.currentTheme == "LIGHT") {
        this.currentTheme = "DARK";
        this.themeSymbol = "🌑";
        this.matrixTheme = {
          backgroundColor: "rgb(39, 39, 39)",
          gridColor: "white",
        };
      } else {
        this.currentTheme = "LIGHT";
        this.themeSymbol = "☀️";
        this.matrixTheme = {
          backgroundColor: "white",
          gridColor: "black",
        };
      }
      this.body.classList.toggle("dark-theme");
    },
  },
});

export const usedLanguage = defineStore("usedLanguage", {
  state: () => {
    let currLang = "EN";
    let currLangFile = ENLang;
    let capacity = currLangFile.capacity;
    let cost = currLangFile.cost;
    let battery = currLangFile.battery;
    let pv = currLangFile.pv;
    let pv_production = currLangFile.pv_production;
    let pv_curtailment = currLangFile.pv_curtailment;
    let demand = currLangFile.demand;
    let purchased_power = currLangFile.purchased_power;
    let storage_text = currLangFile.storage_text;
    let storage_charge = currLangFile.storage_charge;
    let storage_discharge = currLangFile.storage_discharge;
    let storage_level = currLangFile.storage_level;
    let simulate = currLangFile.simulate;
    let reset_text = currLangFile.reset_text;
    let auto = currLangFile.auto;
    let title_upper_plot = currLangFile.title_upper_plot;
    let title_middle_plot = currLangFile.title_middle_plot;
    let title_lower_plot = currLangFile.title_lower_plot;
    let load_scenario = currLangFile.load_scenario;
    let upload_scenario = currLangFile.upload_scenario;
    let toggle_grid = currLangFile.toggle_grid;
    let add_consumer = currLangFile.add_consumer;
    let add_energy_source = currLangFile.add_energy_source;
    let clear_nodes = currLangFile.clear_nodes;
    let save_text = currLangFile.save_text;
    let lock_text = currLangFile.lock_text;
    let unlock_text = currLangFile.unlock_text;
    let add_edge = currLangFile.add_edge;
    let upload_json = currLangFile.upload_json;
    let selector_text_consumer = currLangFile.selector_text_consumer;
    let selector_text_producer = currLangFile.selector_text_producer;

    return {
      currLang,
      currLangFile,
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
      save_text,
      lock_text,
      unlock_text,
      add_edge,
      upload_json,
      selector_text_consumer,
      selector_text_producer,
      storage_text,
    };
  },
  actions: {
    changeLang(language) {
      console.log("Change has been called!");
      if (this.currLang == language) {
        return;
      }
      if (language == "EN") {
        console.log("Changed to EN");
        this.currLang = "EN";
        this.currLangFile = ENLang;
      } else if (language == "DE") {
        console.log("Changed to DE");
        this.currLang = "DE";
        this.currLangFile = DELang;
      } else {
        return;
      }
      this.capacity = this.currLangFile.capacity;
      this.cost = this.currLangFile.cost;
      this.battery = this.currLangFile.battery;
      this.pv = this.currLangFile.pv;
      this.pv_production = this.currLangFile.pv_production;
      this.pv_curtailment = this.currLangFile.pv_curtailment;
      this.demand = this.currLangFile.demand;
      this.purchased_power = this.currLangFile.purchased_power;
      this.storage_text = this.currLangFile.storage_text;
      this.storage_charge = this.currLangFile.storage_charge;
      this.storage_discharge = this.currLangFile.storage_discharge;
      this.storage_level = this.currLangFile.storage_level;
      this.simulate = this.currLangFile.simulate;
      this.reset_text = this.currLangFile.reset_text;
      this.auto = this.currLangFile.auto;
      this.title_upper_plot = this.currLangFile.title_upper_plot;
      this.title_middle_plot = this.currLangFile.title_middle_plot;
      this.title_lower_plot = this.currLangFile.title_lower_plot;
      this.load_scenario = this.currLangFile.load_scenario;
      this.upload_scenario = this.currLangFile.upload_scenario;
      this.toggle_grid = this.currLangFile.toggle_grid;
      this.add_consumer = this.currLangFile.add_consumer;
      this.add_energy_source = this.currLangFile.add_energy_source;
      this.clear_nodes = this.currLangFile.clear_nodes;
      this.save_text = this.currLangFile.save_text;
      this.lock_text = this.currLangFile.lock_text;
      this.unlock_text = this.currLangFile.unlock_text;
      this.add_edge = this.currLangFile.add_edge;
      this.upload_json = this.currLangFile.upload_json;
      this.selector_text_consumer = this.currLangFile.selector_text_consumer;
      this.selector_text_producer = this.currLangFile.selector_text_producer;
    },
  },
});
