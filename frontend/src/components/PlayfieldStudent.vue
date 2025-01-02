<template>
  <Panel id="playfieldS">
     <div
      id="vueflow_container"
      ref="vueFlowContainer"
      :style="{
        backgroundImage: 'url(' + imgUrl + ')',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
      }"
      style="
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 43rem;
        z-index: 2;
      "
    >
      <vue-flow
        v-model:nodes="nodes"
        v-model:edges="edges"
        :fit-view="true"
        :zoomOnScroll="false"
        :zoomOnPinch="false"
        :panOnDrag="false"
        :pan-on-scroll="false"
        :preventScrolling="true"
        :snap-grid="snapGrid"
        :snap-to-grid="true"
      
        :connection-mode="connectionMode"
        :node-types="customNodeTypes"
        :auto-pan-on-node-drag="false"
        :nodes-draggable="!locked"
        :edges-connectable="edgeMode"
        :zoomOnDoubleClick="false"
        @connect="onConnect"
      />
    </div>

    <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay"></canvas>

    <!-- Buttons at the Bottom -->

    <div id="buttons_container">
      <Select
        v-model="selectedProducer"
        :options="scenarios"
        class="slider-button"
        placeholder="Choose Scenario"
      ></Select>
      <Button
        @click="loadRequest"
        type="submit"
        class="slider-button"
        v-bind:label="load_scenario"
      ></Button>
      <Button
        @click="triggerImageUpload"
        type="submit"
        class="slider-button"
        v-bind:label="upload_scenario"
        ></Button
      >
      <Button
        @click="triggerJsonUpload"
        type="submit"
        class="slider-button"
        v-bind:label="upload_json"
        ></Button
      >
      <Button
        @click="toggleGridOverlay"
        type="submit"
        class="slider-button"
        v-bind:label="toggle_grid"
      ></Button>
    </div>
    <input
      type="file"
      id="imageInput"
      ref="imageInput"
      @change="handleFileChange('image', $event)"
      accept="image/*"
      style="display: none"
    />
    <input
      type="file"
      id="jsonInput"
      ref="jsonInput"
      @change="handleFileChange('json', $event)"
      accept=".json"
      style="display: none"
    />
  </Panel>
</template>

<script>
import { Button,Select } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";
import { VueFlow } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";
import ConsumerNode from "./customNodes/Consumer.vue";
import ConsumerIcon from "@/assets/9sg0t-5fb6x-001.ico";
import { inject } from "vue";

export default {
  components: {
    Panel,
    Button,
    VueFlow,
    Select,
  },
  setup() {
    let load_scenario = inject("load_scenario");
    let upload_scenario = inject("upload_scenario");
    let upload_json = inject("upload_json");
    let toggle_grid = inject("toggle_grid");
    return {
      load_scenario,
      upload_scenario,
      upload_json,
      toggle_grid,
    };
  },
  data() {
    return {
      imgUrl: null, // URL for the image
      showGrid: false, // Flag for showing grid
      gridSize: 15, // Grid size (number of cells per row/column)
      nodes: [], // Nodes for Vue Flow
      edges: [], // Edges for Vue Flow
      customNodeTypes: {
        consumer: ConsumerNode,
      }, // Define custom node types if needed
      nodeIdCounter: 1, // Counter for unique IDs
      connectionMode: "strict", // Connection mode for the graph
      edgeMode: false, // Flag to track if edge creation mode is activated
      selectedNodeId: null, // Track the selected node for edge creation
      edgeProps: {
        // Default edge properties (adjustable)
        color: "#000000", // Edge color
        animated: true, // Edge animation
        style: { strokeWidth: 5 }, // Edge style
      },
      locked: false, // Lock flag

      jsonUrl: null,
      scenarios:["Scene 1", "Scene 2", "Scene 3"]
      
      
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
      this.showGrid = !this.showGrid;
      if (this.showGrid) {
        this.$nextTick(() => {
          this.drawGrid(); // Ensure grid is drawn when visible
        });
      }
    },

    drawGrid() {
      const canvas = this.$refs.gridCanvas;
      const vueFlowContainer = this.$refs.vueFlowContainer;

      if (!canvas || !vueFlowContainer) return;

      // Match canvas dimensions to the VueFlow container
      const width = vueFlowContainer.offsetWidth;
      const height = vueFlowContainer.offsetHeight;

      canvas.width = width;
      canvas.height = height;

      const cellWidth = width / this.gridSize;
      const cellHeight = height / this.gridSize;

      // Set the snapGrid based on cell width/height
      this.snapGrid = [cellWidth, cellHeight]; // Update snapGrid

      const context = canvas.getContext("2d");
      context.clearRect(0, 0, width, height); // Clear the canvas
      context.strokeStyle = "#000000"; // Set grid line color
      context.lineWidth = 1; // Set grid line width

      // Draw vertical lines
      for (let x = 0; x <= width; x += cellWidth) {
        context.beginPath();
        context.moveTo(x, 0);
        context.lineTo(x, height);
        context.stroke();
      }

      // Draw horizontal lines
      for (let y = 0; y <= height; y += cellHeight) {
        context.beginPath();
        context.moveTo(0, y);
        context.lineTo(width, y);
        context.stroke();
      }
    },

    async saveData() {
      try {
        // Get node and edge data
        const dataToSave = {
          nodes: this.nodes.map((node) => ({
            id: node.id,
            position: node.position,
            type: node.type,
            label: node.data.label,
          })),
          edges: this.edges.map((edge) => ({
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

        // Send to backend (Django)

        const url = "http://127.0.0.1:8000/api/save-scenario/";
        const response = await axios.post(
          url,
          {
            data: dataToSave,
          },
          {
            headers: {
              "Content-Type": "application/json", // Ensures JSON format
            },
          }
        );

        if (response.status === 200) {
          alert("Data saved successfully!");
        } else {
          alert("Error saving data.");
        }

        // Optionally, download the JSON file
        const jsonString = JSON.stringify(dataToSave);

        const jsonBlob = new Blob([jsonString], { type: "application/json" });
        const jsonLink = document.createElement("a");
        jsonLink.href = URL.createObjectURL(jsonBlob);
        jsonLink.download = "scenario_data.json";
        jsonLink.click();

        // Save image file locally
        const imageLink = document.createElement("a");
        imageLink.href = URL.createObjectURL(this.imageFile);
        imageLink.download = this.imageFile.name || "scenario_image.png";
        imageLink.click();

        alert("Files downloaded locally!");
      } catch (error) {
        console.error("Error saving data:", error);
        alert(`Error: ${error.message}`);
      }
    },

    // Handle file changes for both image and JSON
    triggerImageUpload() {
      this.$refs.imageInput.click(); // Trigger image upload
    },

    // Trigger the JSON file input
    triggerJsonUpload() {
      this.$refs.jsonInput.click(); // Trigger JSON upload
    },

    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (type === "image") {
        this.imageFile = file;
        if (this.imgUrl) URL.revokeObjectURL(this.imgUrl);
        this.imgUrl = URL.createObjectURL(file);

        // Show alert for JSON upload
        alert("Please upload the corresponding JSON file.");
      } else if (type === "json") {
        this.jsonFile = file;
        this.loadScenarioData(); // Handle JSON after image upload
      }
    },

    // Load and parse the JSON file
    loadScenarioData() {
      if (!this.imageFile || !this.jsonFile) {
        alert("Please upload both the image and the JSON file.");
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          this.nodes = data.nodes || [];
          this.edges = data.edges || [];
        } catch (error) {
          console.error("Error parsing JSON:", error);
          alert("Invalid JSON file.");
        }
      };
      reader.readAsText(this.jsonFile);
    },
  },
};
</script>

<style>

/* Playfield Styles */
#playfieldS {
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

#buttons_container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  width: auto;
  height: 2rem;
  position: absolute;
  bottom: 0;

  background-color: var(--primary-background-color);
  z-index: 3;
}

 .p-button-label {
  color: black;
}
.slider-button {
  margin-bottom: 10px;
  margin-right: 5px;
}



#vueflow_container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 42rem;
  z-index: 2;
  overflow: hidden;
}

#grid_overlay {
  position: absolute;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 3;
  width: 100%;
  height: 91.85%;
}
</style>


