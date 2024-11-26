<template>
  <Panel header="Playfield">
    <img
      src="../assets/Shlerp.gif"
      style="min-height: 10%; max-height: 40%; min-width: 10%; max-width: 40%; object-fit: contain;"
    />
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
