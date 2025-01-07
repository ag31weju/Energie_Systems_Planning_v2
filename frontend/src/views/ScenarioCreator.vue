<template>
  <div id="drawerbox">
    <Drawerbox @changeLanguage="updateLanguage"></Drawerbox>
  </div>
  <div id="rootdiv" class="grid-row">
    <div id="outercolumn1" class="grid-column">
      <div id="imagebox1" class="grid-column">
        <Playfield></Playfield>
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
import Drawerbox from "@/components/Drawerbox.vue";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  setup() {
    return {};
  },
  components: {
    Playfield,
    NodeSelector,
    Drawerbox,
  },
  methods: {

  },
};
</script>
<style>
@import "../assets/main.css";
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