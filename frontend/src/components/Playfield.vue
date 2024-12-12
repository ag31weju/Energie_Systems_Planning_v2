<template>
  <Panel id="playfield">
    <div id="image_box">
      <img
        id="base_image"
        :src="imgUrl"
        style="min-height: 10%; max-height: 65%; min-width: 10%; max-width: 75%"
      />
      <!-- <img
        v-for="(marker, index) in markers"
        :key="index"
        :src="marker.src"
        :style="getStyleAndPos(marker)"
        class="overlay_image"
      /> -->
    </div>
    <Button @click="loadRequest" type="submit" class="button"
    v-bind:label="load_scenario"></Button>
  </Panel>
</template>

<script>
import { Button } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";

export default {
  props: [ 'load_scenario' ],
  data() {
    return {
      imgUrl: null,
      markers: [],
      tile_width: 0,
      tile_height: 0,
    };
  },
  components: {
    Panel,
    Button,
  },
  beforeUnmount() {
    //revoke URL after the Playfield Component has been unmounted, so that it can be immediately be used afterwards
    if (this.imageUrl) {
      URL.revokeObjectURL(this.imageUrl);
    }
  },
  methods: {
    getStyleAndPos(marker) {
      return {
        position: "absolute",
        top: `${marker.y}px`,
        left: `${marker.x}px`,
        width: `${this.tile_width}px`,
        height: `${this.tile_height}px`,
      };
    },

    async loadRequest() {
      try {
        const url = "http://127.0.0.1:8000/api/process-scenario/"; //If frontend and backend have different ports, use the full URL
        const id = 1;

        //get JSON file
        const graphResponse = await axios.get(url, {
          params: { id: id, filetype: "json" },
          responseType: "json",
        });

        const graphData = graphResponse.data;
        const grid_size = graphData["grid_size"];
        const nodes = graphData["nodes"];
        const edges = graphData["edges"];

        //get image file
        const imgResponse = await axios.get(url, {
          params: { id: id, filetype: "png" },
          responseType: "blob",
        });

        if (this.imageUrl) {
          //revoke old, unused URL so that Urls aren't unnecessarily reserved
          URL.revokeObjectURL(this.imageUrl);
        }

        this.imgUrl = URL.createObjectURL(imgResponse.data); //URL for img element to use

        const imgElement = document.getElementById("base_image");

        //The image needs to be loaded first, so that the correct, fully-loaded dimensions are used for further computation
        imgElement.onload = () => {
          //Whole, rounded integers
          const width = imgElement.offsetWidth; //left background image
          const height = imgElement.offsetHeight; //top background image
          this.tile_width = width / grid_size;
          this.tile_height = height / grid_size;
          console.log(width, height, this.tile_width, this.tile_height);

          this.markers = []; //reset it to empty
          nodes.forEach((node) => {
            const markerX = Math.round(node.x * this.tile_width);
            const markerY = Math.round(node.y * this.tile_height);
            const imgSrc = "markers/marker1.png";

            this.markers.push({ src: imgSrc, x: markerX, y: markerY });
          });
        };
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
