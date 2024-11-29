<template>
  <Panel id="checkboxes-container">
    <div id="checkboxes" class="grid-column">
      <div id="cbrow" class="grid-column">
        <input type="checkbox" class="checkbox" /> Option 1
        <input type="checkbox" class="checkbox" /> Option 2
        <input type="checkbox" class="checkbox" /> Option 3
      </div>
      <div id="cbrow" class="grid-column">
        <input type="checkbox" class="checkbox" /> Option 4
        <input type="checkbox" class="checkbox" /> Option 5
        <input type="checkbox" class="checkbox" /> Option 6
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
