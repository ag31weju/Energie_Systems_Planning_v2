<template>
  <div id="Drawerbox">
    <Drawerbox @changeLanguage="updateLanguage"></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox" class="grid-column">
        <Playfield v-bind:load_scenario="load_scenario" v-bind:upload_scenario="upload_scenario"
          v-bind:toggle_grid="toggle_grid" v-bind:add_consumer="add_consumer"
          v-bind:add_energy_source="add_energy_source" v-bind:clear_nodes="clear_nodes" />
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="nodebox" class="grid-column">
        <NodeSelector />
      </div>
    </div>
  </div>
</template>


<script>
import { ref } from "vue";
import Playfield from "../components/Playfield.vue";
import NodeSelector from "@/components/NodeSelector.vue";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  setup() {
    return {};
  },
  components: {
    Playfield,
    NodeSelector,
  },
  methods: {

  },
};
</script>
<style>
#nodebox {
  display: flex;
  /* Use flexbox for alignment */
  justify-content: center;
  /* Center horizontally */
  align-items: center;
  /* Center vertically */
  height: 100%;
  /* Ensure it spans the full height */
  width: 100%;
  /* Ensure it spans the full width */
}
</style>