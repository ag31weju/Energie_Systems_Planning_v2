<template>
  <Panel id="checkboxes-container">
    <div id="checkboxes" class="grid-column">
      <div id="cbrow" class="grid-column">
        <input type="checkbox" class="checkbox" /> PV Production
        <input type="checkbox" class="checkbox" /> PV Curtailment
        <input type="checkbox" class="checkbox" /> Purchased Power
      </div>
      <div id="cbrow" class="grid-column">
        <input type="checkbox" class="checkbox" /> Demand
        <input type="checkbox" class="checkbox" /> Storage Charge
        <input type="checkbox" class="checkbox" /> Storage Discharge
      </div>
    </div>
  </Panel>
</template>

<script>
import Panel from "primevue/panel";

export default {
  components: {
    Panel,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
