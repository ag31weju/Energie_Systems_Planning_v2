<template>
  <Panel id="playfield">
    <Button @click="loadRequest" type="submit" class="slider-button">Load Scenario</Button>
    <img src="../assets/Shlerp.gif" style="min-height: 10%; max-height: 50%; min-width: 10%; max-width: 50%" />
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
        const url = "http://127.0.0.1:8000/api/process-scenario/"; //If frontend and backend have different ports, use the full URL
        const data = await fetch("scenarios/scene1.json").then((file) =>
          file.json()
        );
        const response = await axios.post(url, data);
        console.log("Response:", response.data);
        // Display a popup with the backend's message
        alert(`Backend says: ${response.data.message}`);
      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Backend says: ${response.data.message}`);
      }
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
