<template>
  <Panel id="playfield">
    <!-- Image Box -->
    <div id="image_box" ref="imageBox">
      <!-- Display Image -->
      <img :src="imgUrl" style="max-width: 100%; max-height: 100%; object-fit: fill" ref="imageElement" />

      <!-- Sigma.js Container -->
      <div ref="sigmaContainer" id="sigma_overlay"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: auto; z-index: 1;">
      </div>
    </div>

    <!-- Buttons at the Bottom -->
    <div id="buttons_container">
      <Button @click="loadRequest" type="submit" class="slider-button" v-bind:label="load_scenario"></Button>
      <Button @click="initSigma" type="submit" class="slider-button">Show Graph</Button>
      <Button @click="triggerFileUpload" type="button" class="slider-button" v-bind:label="upload_scenario"></Button>
    </div>

    <!-- File Inputs (Hidden) -->
    <!-- File Inputs (Hidden) -->
    <input type="file" id="imageInput" ref="imageInput" @change="handleFileChange('image', $event)" accept="image/*"
      style="display: none;" />
    <input type="file" id="jsonInput" ref="jsonInput" @change="handleFileChange('json', $event)" accept=".json"
      style="display: none;" />

  </Panel>
</template>

<script>
import { Button } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";
import Sigma from "sigma";
import { Graph } from "graphology";

export default {
  props: [
    "upload_scenario",
    "load_scenario",
  ],
  components: {
    Panel,
    Button,
  },
  data() {
    return {
      imgUrl: null, // URL for the image
      showGrid: false, // Flag for showing grid
      gridSize: 15, // Grid size (number of cells per row/column)

      imageFile: null, // To store selected image
      jsonFile: null, // To store selected JSON file

      sigmaInstance: null, // Reference to the Sigma.js instance
      isGraphDrawn: false,
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



    //Start---Scenario Upload------//
    //Start---Scenario Upload------//
    triggerFileUpload() {
      // First trigger the image input picker
      alert("Please upload scenario image and json");
      this.$refs.imageInput.click();
    },

    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (type === "image") {
        this.imageFile = file;
        // Convert the selected image file into a URL for display
        if (this.imgUrl) {
          URL.revokeObjectURL(this.imgUrl); // Clean up the previous object URL if any
        }
        // After selecting the image, trigger the JSON file picker
        if (file) {
          this.$refs.jsonInput.click();
        }
      } else if (type === "json") {
        this.jsonFile = file;

        // If both files are selected, proceed to upload
        if (this.imageFile && this.jsonFile) {
          this.uploadFiles();
        }
      }
    },


    async uploadFiles() {
      if (!this.imageFile || !this.jsonFile) {
        alert("Please select both an image and a JSON file.");
        return;
      }

      try {
        const url = "http://127.0.0.1:8000/api/upload_files/";
        const formData = new FormData();

        formData.append("image", this.imageFile);
        formData.append("json", this.jsonFile);

        const response = await axios.post(url, formData, {
          headers: { "Content-Type": "multipart/form-data" },
          responseType: "blob", // Expect a blob (binary data) from the server
        });

        // Convert the blob response into a URL and set imgUrl
        if (this.imgUrl) {
          URL.revokeObjectURL(this.imgUrl); // Clean up any previous object URL
        }

        this.imgUrl = URL.createObjectURL(response.data);

        alert("Image & Json successfully processed and updated!");

      } catch (error) {
        console.error("Error uploading files:", error);
        alert("Failed to upload files. Please try again.");
      }
    },


    //End---Scenario Upload------//

    //SigmaJs
    initSigma() {
      const graph = new Graph();

      // Get image and canvas dimensions
      // Get image and canvas dimensions
      const imgElement = this.$refs.imageElement;
      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;
      const cellWidth = width / 15;
      const cellHeight = height / 15;

      // Define your nodes with grid-based coordinates
      const nodes = [
        { id: "node1", gridX: 1, gridY: 0, label: "A", color: "#FF0000" },
        { id: "node2", gridX: 5, gridY: 5, label: "B", color: "#00FF00" },
        { id: "node3", gridX: 9, gridY: 10, label: "C", color: "#0000FF" },
        { id: "node4", gridX: 2, gridY: 2, label: "D", color: "#FF0000" },
        { id: "node5", gridX: 1, gridY: 8, label: "E", color: "#00FF00" },
        { id: "node6", gridX: 1, gridY: 5, label: "F", color: "#0000FF" },
      ];

      // Add nodes to the graph
      nodes.forEach((node) => {
        // Adjust coordinates to center the grid in Sigma's coordinate system
        const nodeX = (node.gridX * cellWidth) + (cellWidth / 2); // Center horizontally
        const nodeY = (node.gridY * cellHeight) + (cellHeight / 2); // Center vertically

        graph.addNode(node.id, {
          x: nodeX,
          y: nodeY,
          size: 10,
          label: node.label,
          color: node.color,
        });
      });

      // Optional: Add edges
      graph.addEdge("node1", "node2", { size: 3 });
      graph.addEdge("node2", "node3", { size: 3 });

      // Initialize Sigma.js
      const container = this.$refs.sigmaContainer;

      if (!container) {
        console.error("Sigma container not found!");
        return;
      }

      container.style.width = `${width}px`;
      container.style.height = `${height}px`;

      // Create the Sigma.js instance
      if (!this.isGraphDrawn) {
        this.sigmaInstance = new Sigma(graph, container, {
          enablePan: false, // Disable panning
          enableZoom: false, // Disable zoom
          enableEdgeHoverEvents: true, // Enable edge hover events
          enableCameraPanning: false,
          enableCameraZooming: false,
        });
        this.isGraphDrawn = true; // Update the reactive property
      }



      // Add click and hover events for nodes
      this.sigmaInstance.on("clickNode", ({ node }) => {
        alert(`Node clicked: ${graph.getNodeAttribute(node, "label")}`);
      });

      this.sigmaInstance.on("enterNode", ({ node }) => {
        // Get node attributes
        const nodeLabel = graph.getNodeAttribute(node, "label");
        const nodeX = graph.getNodeAttribute(node, "x");
        const nodeY = graph.getNodeAttribute(node, "y");

        // Highlight the node and display its label and position

        console.log(`Node: ${nodeLabel}, Position: (${nodeX.toFixed(2)}, ${nodeY.toFixed(2)})`);
      });

      //  this.sigmaInstance.on("leaveNode", ({ node }) => {
      //    const originalColor = graph.getNodeAttribute(node, "color"); // Get the original color
      //    this.sigmaInstance.getGraph().setNodeAttribute(node, "color", originalColor); // Reset color
      // });

      console.log("Sigma graph initialized with panning disabled.");
    },
  },


};
</script>

<style>
/* Playfield Styles */
#playfield {
  display: flex;
  flex-direction: column;
  /* Stack elements vertically */
  justify-content: flex-start;
  /* Align items to the top */
  align-items: stretch;
  width: 100%;
  height: 100%;
  background-color: var(--primary-background-color);
  border: var(--primary-border);
  position: relative;
  /* Set relative positioning to position the buttons container absolutely */
}


#grid_overlay {
  position: relative;
  /* Overlay on top of the image */
  top: 0;
  left: 0;
  pointer-events: none;
  /* Allow clicks to pass through the canvas */
  z-index: 1;
}

#buttons_container {
  display: flex;
  flex-direction: row;
  /* Stack buttons vertically */
  justify-content: center;
  /* Center buttons vertically */
  align-items: center;
  /* Center buttons horizontally */
  width: 100%;
  height: auto;
  /* Height adjusts to the button content */
  position: absolute;
  /* Fix the position at the bottom of the playfield */
  bottom: 0;
  /* Position it at the bottom */
  padding: 10px;
  /* Add padding for spacing */
  background-color: var(--primary-background-color);
  /* Add a border on top to separate from the image box */
  /* Add a border on top to separate from the image box */
}

.slider-button {
  margin-bottom: 5px;
  /* Reduced space between buttons */
}

.slider-button .p-button-label {
  color: black;
}

#vueflow_container {
  position: relative;
  top: 0;
  left: 0;
  pointer-events: auto;
  /* Allow interaction */
  z-index: 2;
  overflow: hidden;
}
</style>
