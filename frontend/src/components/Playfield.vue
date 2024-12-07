<template>
  <Panel id="playfield">
    <!-- Image Box and Sigma Container -->
    <div id="image_box">
      <!-- Display Image -->
      <img
        :src="imgUrl"
        style="max-width: 100%; max-height: 100%; object-fit: contain;"
        ref="imageElement"
      />

      <!-- Sigma Container for Graph -->
      <div v-if="showGrid" id="sigma_container"></div>

      <!-- Grid Overlay with Labels -->
      <div v-if="showGrid" id="grid_overlay">
        <!-- Dynamically generate grid labels -->
        <div v-for="x in gridSize" :key="'x-' + x" :class="['grid-label', 'x-label']" :style="{ left: `${x * spacing}px` }">{{ x }}</div>
        <div v-for="y in gridSize" :key="'y-' + y" :class="['grid-label', 'y-label']" :style="{ top: `${y * spacing}px` }">{{ y }}</div>
      </div>
    </div>

    <!-- Buttons at the Bottom -->
    <div id="buttons_container">
      <Button @click="loadRequest" type="submit" class="slider-button">Load Scenario</Button>
      <Button @click="toggleCoordinateSystem" type="submit" class="slider-button" style="margin-left: 10px;">
        Toggle Grid
      </Button>
    </div>
  </Panel>
</template>

<script>
import { Button } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";
import Sigma from "sigma";
import Graph from "graphology";

export default {
  data() {
    return {
      imgUrl: null, // URL for the image
      showGrid: false, // Flag to toggle the grid
      sigmaInstance: null, // Sigma instance for rendering the graph
      graph: null, // Graphology graph object
      gridSize: 10, // Grid size (15x15 by default)
      spacing: 0, // Spacing between nodes (calculated dynamically)
    };
  },
  components: {
    Panel,
    Button,
  },
  beforeUnmount() {
    // Clean up resources on component unmount
    if (this.imgUrl) {
      URL.revokeObjectURL(this.imgUrl);
    }
    if (this.sigmaInstance) {
      this.sigmaInstance.kill();
    }
  },
  methods: {
    async loadRequest() {
      // Fetch the graph data and image
      try {
        const url = "http://127.0.0.1:8000/api/process-scenario/";
        const id = 1;

        const graphResponse = await axios.get(url, {
          params: { id: id, filetype: "json" },
          responseType: "json",
        });

        const imgResponse = await axios.get(url, {
          params: { id: id, filetype: "png" },
          responseType: "blob",
        });

        if (this.imgUrl) {
          URL.revokeObjectURL(this.imgUrl);
        }

        this.imgUrl = URL.createObjectURL(imgResponse.data);

        // Render Sigma graph after image is loaded
        this.$nextTick(() => {
          if (this.showGrid) {
            this.setupSigma();
          }
        });
      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Error: ${error.message}`);
      }
    },
    toggleCoordinateSystem() {
      // Toggle the visibility of the grid
      this.showGrid = !this.showGrid;

      if (this.showGrid) {
        this.$nextTick(() => {
          this.setupSigma();
        });
      } else if (this.sigmaInstance) {
        this.sigmaInstance.kill();
        this.sigmaInstance = null;
      }
    },
    setupSigma() {
      // Initialize the Sigma.js graph rendering
      const container = document.getElementById("sigma_container");
      const imgElement = this.$refs.imageElement;

      if (!container || !imgElement) return;

      // Dynamically calculate spacing based on image size and grid size
      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;

      this.spacing = Math.min(width / this.gridSize, height / this.gridSize);

      const graph = new Graph();

      // Create a fixed grid of nodes
      for (let x = 0; x < this.gridSize; x++) {
        for (let y = 0; y < this.gridSize; y++) {
          graph.addNode(`${x},${y}`, {
            x: x * this.spacing,
            y: y * this.spacing,
            size: 5,
            color: "#000000",
          });
        }
      }

      // Create a new Sigma instance
      if (!this.sigmaInstance) {
        this.sigmaInstance = new Sigma(graph, container, {
          settings: {
            defaultNodeColor: "#FFFFFF",
            enableCamera: false, // Disable camera movement
            mouseEnabled: false, // Disable mouse interaction
          },
        });
      }

      // Adjust container dimensions
      container.style.width = `${width}px`;
      container.style.height = `${height}px`;
    },
  },
};
</script>

<style>
/* Playfield Styles */
#playfield {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: stretch;
  width: 100%;
  height: 100%;
  background-color: var(--primary-background-color);
  border: var(--primary-border);
}

#image_box {
  flex-grow: 1; /* Take up all remaining space */
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  width: 100%;
  height: auto;
  background-color: #f4f4f4;
  border-bottom: 1px solid #ccc;
  overflow: hidden; /* Prevent content from overflowing */
}

#sigma_container {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none; /* Disable user interaction */
}

#buttons_container {
  display: flex;
  justify-content: center;
  padding: 10px;
  background-color: var(--primary-background-color);
}

/* Grid Overlay Styles */
#grid_overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-wrap: wrap;
  pointer-events: none;
}

.grid-label {
  position: absolute;
  font-size: 12px;
  color: rgba(0, 0, 0, 0.5);
}

.x-label {
  top: -20px;
  left: 0;
}

.y-label {
  left: -20px;
  top: 0;
}
</style>
