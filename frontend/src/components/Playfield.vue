<template>
  <Panel id="playfield">
    <Button @click="loadRequest" type="submit" class="slider-button"
      >Load Scenario</Button
    >
    <img
      src="../assets/Shlerp.gif"
      style="min-height: 10%; max-height: 50%; min-width: 10%; max-width: 50%"
    />
  </Panel>
</template>

<script>
import { Button } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";

export default {
  components: {
    Panel,
    Button,
  },
  methods: {
    async loadRequest() {
      try {
        const url = "scenarios/example.json";
        const data = await fetch("scenarios/scene1.json").then((file) =>
          file.json()
        );
        const response = await axios.post(url, data);
        console.log("Response:", response.data);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
