<template>
  <Panel id="playfield">
    <!-- Image Box -->
    <div id="image_box" ref="imageBox">
      <!-- Display Image -->
      <img :src="imgUrl" style="max-width: 100%; max-height: 100%; object-fit: fill" ref="imageElement" />

      <!-- Canvas for Grid Overlay -->
      <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay"
        style="position: absolute; top: 0; left: 0; pointer-events: none; z-index: 1;"></canvas>

      <!-- Vue Flow Container -->
      <div id="vueflow_container" ref="vueFlowContainer"
        style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 2;">
        <vue-flow v-model:nodes="nodes" v-model:edges="edges" :fit-view="true" :zoom-on-scroll="false"
          :zoom-on-pinching="false" :pan-on-drag="false" :pan-on-scroll="false" :prevent-scrolling="true"
          :coordinate-extent="coordinateExtent" :connection-mode="connectionMode" :node-types="customNodeTypes"
          :nodes-draggable="!locked" :edges-connectable="!locked" @connect="onConnect" />
      </div>
    </div>

    <!-- Buttons at the Bottom -->
    <div id="buttons_container">
      <Button @click="loadRequest" type="submit" class="slider-button" v-bind:label="load_scenario"></Button>
      <Button @click="toggleGridOverlay" type="submit" class="slider-button" v-bind:label="toggle_grid"></Button>
      <Button @click="addConsumerNode" type="submit" class="slider-button" v-bind:label="add_consumer"></Button>
      <Button @click="addEnergySourceNode" type="submit" class="slider-button"
        v-bind:label="add_energy_source"></Button>
      <Button @click="toggleEdgeMode" type="submit" class="slider-button" v-bind:label="add_edge">Edge mode</Button>
      <Button @click="toggleLock" type="submit" class="slider-button"
        v-bind:label="locked ? 'Unlock' : 'Lock'">TL</Button>
      <Button @click="clearNodes" type="submit" class="slider-button" v-bind:label="clear_nodes"></Button>
      <Button @click="saveData" type="submit" class="slider-button" v-bind:label="'Save'"></Button>
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

export default {
  props: [
    "upload_scenario",
    "load_scenario",
    "toggle_grid",
    "add_consumer",
    "add_energy_source",
    "clear_nodes",
    "add_edge",
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
      nodes: [], // Nodes for Vue Flow
      edges: [], // Edges for Vue Flow
      customNodeTypes: {}, // Define custom node types if needed
      nodeIdCounter: 1, // Counter for unique IDs
      connectionMode: "strict", // Connection mode for the graph
      edgeMode: false, // Flag to track if edge creation mode is activated
      selectedNodeId: null, // Track the selected node for edge creation
      edgeProps: { // Default edge properties (adjustable)
        color: "#000000", // Edge color
        animated: true, // Edge animation
        style: { strokeWidth: 5 }, // Edge style
      },
      locked: false, // Lock flag
    };
  },


  methods: {
    toggleLock() {
      this.locked = !this.locked;
    },

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

      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;
      canvas.width = width;
      canvas.height = height;

      const context = canvas.getContext("2d");
      const cellWidth = width / this.gridSize;
      const cellHeight = height / this.gridSize;

      context.clearRect(0, 0, width, height);
      context.strokeStyle = "#000000";
      context.lineWidth = 1;

      for (let x = 0; x <= this.gridSize; x++) {
        const xPos = x * cellWidth;
        context.beginPath();
        context.moveTo(xPos, 0);
        context.lineTo(xPos, height);
        context.stroke();
      }

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

      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;

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

      const width = imgElement.offsetWidth;
      const height = imgElement.offsetHeight;

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "energySource",
        position: { x: (2 * width) / 3, y: (2 * height) / 3 },
        data: { label: `EnergySource` },
        style: { backgroundColor: "#33FF57", color: "#000000", padding: "10px", borderRadius: "5px" },
      };
      this.nodes.push(newNode);
    },
    toggleEdgeMode() {
      // Toggle edge creation mode
      this.edgeMode = !this.edgeMode;
      if (this.edgeMode) {
        this.selectedNodeId = null;
        this.connectionMode = "loose"; // Allow loose connections for edge creation
      } else {
        this.connectionMode = "strict"; // Return to strict mode
      }
    },
    clearNodes() {
      this.nodes = [];
      this.edges = [];
    },

    onConnect(connection) {
      if (this.edgeMode) {
        const newEdge = {
          id: `edge_${this.edges.length + 1}`,
          source: connection.source,
          target: connection.target,
          type: "default",
          animated: this.edgeProps.animated,
          style: this.edgeProps.style,
          color: this.edgeProps.color,
        };
        this.edges.push(newEdge);
      }
    },
    async saveData() {
      try {
        // Get node and edge data
        const dataToSave = {
          nodes: this.nodes.map(node => ({
            id: node.id,
            position: node.position,
            type: node.type,
            label: node.data.label,
          })),
          edges: this.edges.map(edge => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            color: edge.color,
            style: edge.style,
          })),
          imageUrl: this.imgUrl,
        };

        // Convert to JSON


        // Send to backend (Django)

        const url = "http://127.0.0.1:8000/api/save-scenario/";
        const response = await axios.post(url, {
          data: dataToSave,
        },
          {
            headers: {
              "Content-Type": "application/json", // Ensures JSON format
            },
          });

        if (response.status === 200) {
          alert("Data saved successfully!");
        } else {
          alert("Error saving data.");
        }

        // Optionally, download the JSON file
        const blob = new Blob([jsonData], { type: "application/json" });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = "scenario_data.json";
        link.click();
      }
      catch (error) {
        console.error("Error saving data:", error);
        alert(`Error: ${error.message}`);
      }
    },


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



  },

};
</script>

<style>
/* Playfield Styles */
#playfield {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  width: 100%;
  height: 100%;
  background-color: var(--primary-background-color);
  border: var(--primary-border);
  position: relative;
}

#grid_overlay {
  position: relative;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}

#buttons_container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: auto;
  position: absolute;
  bottom: 0;
  padding: 10px;
  background-color: var(--primary-background-color);
}

.slider-button {
  margin-bottom: 5px;
}

.slider-button .p-button-label {
  color: black;
}

#vueflow_container {
  position: relative;
  top: 0;
  left: 0;
  pointer-events: auto;
  z-index: 2;
  overflow: hidden;
}

</style>
