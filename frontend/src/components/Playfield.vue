<template>
  <Panel id="playfield">
    <!-- Image Box -->
    <div id="image_box" ref="imageBox">
      <!-- Display Image -->
      <img
        :src="imgUrl"
        style="max-width: 100%; max-height: auto; object-fit: contain;"
        ref="imageElement"
      />

      <!-- Canvas for Grid Overlay -->
      <canvas
        v-if="showGrid"
        ref="gridCanvas"
        id="grid_overlay"
        style="position: absolute; top: 0; left: 0; pointer-events: none; z-index: 1;"
      ></canvas>

      <!-- Vue Flow Container -->
      <div
        id="vueflow_container"
        ref="vueFlowContainer"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2;"
      >
        <vue-flow
          v-model:nodes="nodes"
          :fit-view="false"
          :zoom-on-scroll="false"
          :pan-on-drag="false"
          :connection-mode="'strict'"
          :node-types="customNodeTypes"
          @node-dblclick="onNodeDblClick"
        />
      </div>
    </div>

    <!-- Buttons at the Bottom -->
    <div id="buttons_container">
      <Button @click="loadRequest" type="submit" class="slider-button" v-bind:label="load_scenario"></Button>
      <Button @click="toggleGridOverlay" type="submit" class="slider-button">Toggle Grid</Button>
      <Button @click="addConsumerNode" type="submit" class="slider-button">Add Consumer</Button>
      <Button @click="addEnergySourceNode" type="submit" class="slider-button">Add EnergySource</Button>
      <Button @click="clearNodes" type="submit" class="slider-button">Clear Nodes</Button>
    </div>
  </Panel>
</template>

<script>
import { Button } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";
import { VueFlow } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";

export default {
  props: [ 'load_scenario' ],
  components: {
    Panel,
    Button,
    VueFlow,
  },
  data() {
    return {
      imgUrl: null, // URL for the image
      showGrid: false, // Flag for showing grid
      gridSize: 15, // Grid size (number of cells per row/column)
      nodes: [], // Nodes for Vue Flow
      customNodeTypes: {}, // Define custom node types if needed
      nodeIdCounter: 1, // Counter for unique IDs
    };
  },
  methods: {
    async loadRequest() {
      // Fetch the image URL
      try {
        const url = "http://127.0.0.1:8000/api/process-scenario/";
        const id = 1;

        const imgResponse = await axios.get(url, {
          params: { id: id, filetype: "png" },
          responseType: "blob",
        });

        if (this.imgUrl) {
          URL.revokeObjectURL(this.imgUrl);
        }

        this.imgUrl = URL.createObjectURL(imgResponse.data);
      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Error: ${error.message}`);
      }
    },
    toggleGridOverlay() {
      // Toggle the grid visibility
      this.showGrid = !this.showGrid;

      if (this.showGrid) {
        this.$nextTick(() => {
          this.drawGrid();
        });
      }
    },
    drawGrid() {
      const canvas = this.$refs.gridCanvas;
      const imgElement = this.$refs.imageElement;

      if (!canvas || !imgElement) return;

      // Get the rendered dimensions of the image
      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;

      // Update canvas dimensions to match the image
      canvas.width = width;
      canvas.height = height;

      const context = canvas.getContext("2d");
      const cellWidth = width / this.gridSize;
      const cellHeight = height / this.gridSize;

      // Clear any previous drawing on the canvas
      context.clearRect(0, 0, width, height);

      context.strokeStyle = "#000000"; // Set grid line color
      context.lineWidth = 1;

      // Draw vertical grid lines
      for (let x = 0; x <= this.gridSize; x++) {
        const xPos = x * cellWidth;
        context.beginPath();
        context.moveTo(xPos, 0);
        context.lineTo(xPos, height);
        context.stroke();
      }

      // Draw horizontal grid lines
      for (let y = 0; y <= this.gridSize; y++) {
        const yPos = y * cellHeight;
        context.beginPath();
        context.moveTo(0, yPos);
        context.lineTo(width, yPos);
        context.stroke();
      }
    },
    addConsumerNode() {
      const imgElement = this.$refs.imageElement;
      if (!imgElement) return;

      // Get image dimensions
      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;

      // Add a new Consumer node
      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "consumer",
        position: { x: width / 3, y: height / 3 },
        data: { label: `Consumer` },
        style: { backgroundColor: "#FF5733", color: "#FFFFFF", padding: "10px", borderRadius: "5px" },
      };
      this.nodes.push(newNode);
    },
    addEnergySourceNode() {
      const imgElement = this.$refs.imageElement;
      if (!imgElement) return;

      // Get image dimensions
      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;

      // Add a new EnergySource node
      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "energySource",
        position: { x: (2 * width) / 3, y: (2 * height) / 3 },
        data: { label: `EnergySource` },
        style: { backgroundColor: "#33FF57", color: "#000000", padding: "10px", borderRadius: "5px" },
      };
      this.nodes.push(newNode);
    },
    clearNodes() {
      this.nodes = [];
    },
    onNodeDblClick(event) {
      const nodeId = event.id;
      const targetNode = this.nodes.find((n) => n.id === nodeId);
      if (targetNode) {
        const newName = prompt("Enter new name for the node:", targetNode.data.label);
        if (newName) {
          targetNode.data.label = newName;
        }
      }
    },
  },
};
</script>


<style>
/* Playfield Styles */
#playfield {
  display: flex;
  flex-direction: column; /* Stack elements vertically */
  justify-content: flex-start; /* Align items to the top */
  align-items: stretch;
  width: 100%;
  height: 100%;
  background-color: var(--primary-background-color);
  border: var(--primary-border);
  position: relative; /* Set relative positioning to position the buttons container absolutely */
}

#image_box {
  position: absolute;
  top: 0; /* Anchor to the bottom of the parent */
  left: 0;
  width: 100%;
  height: 90%; /* Default height */
  background-color: #f4f4f4;
  overflow: hidden;
  transition: height 0.3s ease; /* Smoothly animate height changes */
}


#grid_overlay {
  position: relative; /* Overlay on top of the image */
  top: 0;
  left: 0;
  pointer-events: none; /* Allow clicks to pass through the canvas */
  z-index: 1;
}


#buttons_container {
  display: flex;
  flex-direction: row; /* Stack buttons vertically */
  justify-content: center; /* Center buttons vertically */
  align-items: center; /* Center buttons horizontally */
  width: 100%;
  height: auto; /* Height adjusts to the button content */
  position: absolute; /* Fix the position at the bottom of the playfield */
  bottom: 0; /* Position it at the bottom */
  padding: 10px; /* Add padding for spacing */
  background-color: var(--primary-background-color);
   /* Add a border on top to separate from the image box */
}

.slider-button {
  margin-bottom: 5px; /* Reduced space between buttons */
}

#vueflow_container {
  position: relative;
  top: 0;
  left: 0;
  pointer-events: auto; /* Allow interaction */
  z-index: 2;
  overflow: hidden;
}


</style>
