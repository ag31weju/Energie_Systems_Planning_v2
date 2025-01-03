<template>
  <Panel id="playfield">
    <!-- Image Box -->

    <!-- Vue Flow Container -->
    <div
      id="vueflow_container"
      ref="vueFlowContainer"
      :style="{
        backgroundImage: 'url(' + imgUrl + ')',
        backgroundSize: 'contain',
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
        :coordinateExtent="coordinateExtent"
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
      <Button
        @click="loadRequest"
        type="submit"
        class="button"
        v-bind:label="load_scenario"
        ></Button
      >
      <Button
        @click="triggerImageUpload"
        type="submit"
        class="button"
        v-bind:label="upload_scenario"
        ></Button
      >
      <Button
        @click="triggerJsonUpload"
        type="submit"
        class="button"
        v-bind:label="upload_json"
        ></Button
      >
      <Button
        @click="toggleGridOverlay"
        type="submit"
        class="button"
        v-bind:label="toggle_grid"
        ></Button
      >
      <Button
        @click="addConsumerNode"
        type="submit"
        class="button"
        v-bind:label="add_consumer"
        ></Button
      >
      <Button
        @click="addEnergySourceNode"
        type="submit"
        class="button"
        v-bind:label="add_energy_source"
      ></Button>
      <Button
        @click="toggleEdgeMode"
        type="submit"
        class="button"
        v-bind:label="add_edge"
        ></Button
      >
      <Button
        @click="clearNodes"
        type="submit"
        class="button"
        v-bind:label="clear_nodes"
      ></Button>
      <Button
        @click="saveData"
        type="submit"
        class="button"
        v-bind:label="save_text"
      ></Button>

      <Select
        v-model="selectedConsumer"
        :options="optionsConsumer"
        placeholder="Please select consumer type"
      >
      </Select>

      <Select
        v-model="selectedProducer"
        :options="optionsProducers"
        placeholder="Please select producer type"
      >
      </Select>
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
import { Button, Select } from "primevue";
import Panel from "primevue/panel";
import axios from "axios";
import { VueFlow } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";
import ConsumerNode from "./customNodes/Consumer.vue";
import ProducerNode from "./customNodes/Producer.vue";
import ConsumerIcon from "@/assets/node_images/consumer/commercial2.png";
import Commercial from "@/assets/node_images/consumer/commercial.png";
import ResidentialLarge from "@/assets/node_images/consumer/residentialLarge.png";
import ResidentialSmall from "@/assets/node_images/consumer/residentialSmall.png";
import Nuclear from "@/assets/node_images/producer/nuclear.png";
import Coal from "@/assets/node_images/producer/coal.png";
import Solar from "@/assets/node_images/producer/solarPanel.png";
import Wind from "@/assets/node_images/producer/windmill.png";
import { inject } from 'vue';

export default {
  components: {
    Panel,
    Button,
    Select,
    VueFlow,
  },
  setup() {
    let load_scenario = inject('load_scenario');
    let upload_scenario = inject('upload_scenario');
    let upload_json = inject('upload_json');
    let toggle_grid = inject('toggle_grid');
    let add_consumer = inject('add_consumer');
    let add_energy_source = inject('add_energy_source');
    let add_edge = inject('add_edge');
    let clear_nodes = inject('clear_nodes');
    let save_text = inject('save_text');
    return {
      load_scenario,
      upload_scenario,
      upload_json,
      toggle_grid,
      add_consumer,
      add_energy_source,
      add_edge,
      clear_nodes,
      save_text
    };
  },
  data() {
    return {
      imgUrl: null, // URL for the image
      showGrid: false, // Flag for showing grid
      gridSize: 15, // Grid size (number of cells per row/column)
      snapGrid: [50, 50],
      nodes: [], // Nodes for Vue Flow
      edges: [], // Edges for Vue Flow
      customNodeTypes: {
        consumer: ConsumerNode,
        producer: ProducerNode,
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
      coordinateExtent: [
        [0, 0],
        [0, 0],
      ],

      selectedConsumer: "", // Selected value for consumers
      optionsConsumer: ["Commercial", "Residential Large", "Residential Small"], // Initial consumer options

      selectedProducer: "", // Selected value for producers
      optionsProducers: ["Nuclear", "Coal", "Solar", "Wind"], // Initial producer options
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

    addEnergySourceNode() {
      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth / this.gridSize;
      const height = vueFlowContainer.offsetHeight / this.gridSize;

      if (!this.selectedProducer) {
        alert("Please select an energy source type before adding a node.");
        return;
      }

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "producer",
        position: { x: width * 5, y: height * 4 },
        data: {}, // To be filled based on producer type
        targetPosition: "left",
        sourcePosition: "right",
      };

      // Use switch to configure the data property
      switch (this.selectedProducer) {
        case "Nuclear":
          newNode.data = {
            label: "Nuclear Power",
            icon: Nuclear, // Add an icon path if available
            inputs: [1], // Example configuration for inputs
            outputs: [0],
            description:
              "Provides large-scale base power with low carbon emissions.",
          };
          break;

        case "Coal":
          newNode.data = {
            label: "Coal Power",
            icon: Coal, // Add an icon path if available
            inputs: [1],
            outputs: [0],
            description: "Traditional fossil fuel energy source.",
          };
          break;

        case "Solar":
          newNode.data = {
            label: "Solar Power",
            icon: Solar, // Add an icon path if available
            inputs: [],
            outputs: [0],
            description: "Generates renewable energy from sunlight.",
          };
          break;

        case "Wind":
          newNode.data = {
            label: "Wind Power",
            icon: Wind, // Add an icon path if available
            inputs: [],
            outputs: [0],
            description: "Generates renewable energy from wind.",
          };
          break;

        default:
          alert("Unknown producer type selected.");
          return;
      }

      this.nodes.push(newNode);
    },

    addConsumerNode() {
      if (!this.selectedConsumer) {
        alert("Please select an option before adding a node.");
        return;
      }

      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth;
      const height = vueFlowContainer.offsetHeight;

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "consumer",
        position: { x: (2 * width) / 3, y: (2 * height) / 3 },
        data: {}, // To be populated by switch case
      };

      // Use switch to set the data field based on the selected producer
      switch (this.selectedConsumer) {
        case "Commercial":
          newNode.data = {
            label: "Commercial",
            icon: Commercial,
            inputs: [0],
            outputs: [0, 1],
          };
          break;

        case "Residential Large":
          newNode.data = {
            label: "Residential Large",
            icon: ResidentialLarge,
            inputs: [0],
            outputs: [0, 1],
          };
          break;

        case "Residential Small":
          newNode.data = {
            label: "Residential Small",
            icon: ResidentialSmall,
            inputs: [0],
            outputs: [0, 1],
          };
          break;

        default:
          alert("Unknown producer type selected.");
          return;
      }

      this.nodes.push(newNode);
    },

    toggleEdgeMode() {
      // Toggle edge creation mode
      this.locked = !this.locked;
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
@import "../assets/main.css";
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
  z-index: 3;
}

.button {
  margin-bottom: 5px;
}

.button .p-button-label {
  color: black;
}

#vueflow_container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 43rem;
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
