<template>
  <Panel id="playfield">
    <Button @click="loadRequest" type="submit" class="slider-button"
      >Load Scenario</Button
    >
    <img
      :src="imgUrl"
      style="min-height: 10%; max-height: 50%; min-width: 10%; max-width: 50%"
    />
  </Panel>
</template>

<script>
import { Button } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";

export default {
  data() {
    return {
      imgUrl: null,
    };
  },
  components: {
    Panel,
    Button,
  },
  beforeUnmount() {
    if (this.imageUrl) {
      URL.revokeObjectURL(this.imageUrl);
    }
  },
  methods: {
    async loadRequest() {
      try {
        const url = "http://127.0.0.1:8000/api/process-scenario/"; //If frontend and backend have different ports, use the full URL
        const id = 1;

        const graphResponse = await axios.get(url, {
          params: { id: id, filetype: "json" },
          responseType: "json",
        });

        console.log("Response:", graphResponse.data); //graph json file

        const imgResponse = await axios.get(url, {
          params: { id: id, filetype: "png" },
          responseType: "blob",
        });

        if (this.imageUrl) {
          URL.revokeObjectURL(this.imageUrl);
        }

        this.imgUrl = URL.createObjectURL(imgResponse.data);

        // Display a popup with the backend's message
        //alert(`Backend says: ${response.data.message}`);*/
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
