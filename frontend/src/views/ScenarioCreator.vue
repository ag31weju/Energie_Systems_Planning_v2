<template>
  <div>
    <h1>Welcome to the Scenario Creator Page</h1>
  </div>

  <div id="drawerbox">
    <Drawerbox @changeLanguage="updateLanguage"></Drawerbox>
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
    </div>
  </div>
</template>

<script>
import Playfield from "../components/Playfield.vue";

export default {
  components: {
    Playfield,
  },
  setup() {
    return {};
  },
};
</script>
<style></style>
