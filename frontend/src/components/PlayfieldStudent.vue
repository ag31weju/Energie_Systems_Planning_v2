<template>
  <Panel id="playfieldS">
    <div id="vueflow_container" ref="vueFlowContainer" :style="{
      backgroundImage: 'url(' + imgUrl + ')',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }" style="
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 43rem;
        z-index: 2;
      ">
      <vue-flow v-model:nodes="nodes" v-model:edges="edges" :fit-view="true" :zoomOnScroll="false" :zoomOnPinch="false"
        :panOnDrag="false" :pan-on-scroll="false" :preventScrolling="true" :snap-grid="snapGrid" :snap-to-grid="true"
        :connection-mode="connectionMode" :node-types="customNodeTypes" :auto-pan-on-node-drag="false"
        :nodes-draggable="locked" :edges-connectable="false" :zoomOnDoubleClick="false" @connect="onConnect" />
    </div>

    <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay"></canvas>

    <!-- Buttons at the Bottom -->

    <div id="buttons_container">
      <Select v-model="selectedProducer" :options="scenarios" class="slider-button"
        placeholder="Choose Scenario"></Select>
      <Button @click="loadRequest" type="submit" class="slider-button" v-bind:label="load_scenario"></Button>
      <Button @click="triggerImageUpload" type="submit" class="slider-button" v-bind:label="upload_scenario"></Button>

      <Button @click="toggleGridOverlay" type="submit" class="slider-button" v-bind:label="toggle_grid"></Button>
    </div>
    <input type="file" id="imageInput" ref="imageInput" @change="handleFileChange('image', $event)" accept="image/*"
      style="display: none" />
    <input type="file" id="jsonInput" ref="jsonInput" @change="handleFileChange('json', $event)" accept=".json"
      style="display: none" />
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
import { inject, ref, reactive } from 'vue';

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

    //Playfield variables
    const imgUrl = ref(null); // URL for the image
    const showGrid = ref(false); // Flag for showing grid
    const gridSize = ref(15); // Grid size (number of cells per row/column)
    const snapGrid = ref([50, 50]);
    const nodes = ref([]); // Nodes for Vue Flow
    const edges = ref([]); // Edges for Vue Flow
    const nodeIdCounter = ref(1); // Counter for unique IDs
    const connectionMode = ref("strict"); // Connection mode for the graph
    const edgeMode = ref(false); // Flag for edge creation mode
    const selectedNodeId = ref(null); // Track the selected node for edge creation
    const locked = ref(false); // Lock flag
    const jsonUrl = ref(null); // JSON file URL
    const scenarios = ref(["Scene 1", "Scene 2", "Scene 3"]); // Scenario options

    // Reactive object for edge properties
    const edgeProps = reactive({
      color: "#000000", // Edge color
      animated: true, // Edge animation
      style: { strokeWidth: 5 }, // Edge style
    });

    // Reactive object for custom node types
    const customNodeTypes = reactive({
      consumer: ConsumerNode,
      producer: ProducerNode,
    });

    // Reactive state for selected consumer/producer and their options
    const selectedConsumer = ref(""); // Selected value for consumers
    const optionsConsumer = ref(["Commercial", "Residential Large", "Residential Small"]); // Consumer options

    const selectedProducer = ref(""); // Selected value for producers
    const optionsProducers = ref(["Nuclear", "Coal", "Solar", "Wind"]); // Producer options

    return {
      load_scenario,
      upload_scenario,
      upload_json,
      toggle_grid,
      //playfield variables
      imgUrl,
      showGrid,
      gridSize,
      snapGrid,
      nodes,
      edges,
      customNodeTypes,
      nodeIdCounter,
      connectionMode,
      edgeMode,
      selectedNodeId,
      edgeProps,
      locked,
      jsonUrl,
      selectedConsumer,
      optionsConsumer,
      selectedProducer,
      optionsProducers,
      scenarios
    };
  },


  methods: {
    async loadRequest() {
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


        const graphResponse = await axios.get(url, {
          params: { id: id, filetype: "json" },
          responseType: "json",
        });





        const { nodes, edges } = graphResponse.data;


        this.nodes = nodes.map((node) => {
          let newNode = {
            ...node,
            data: {},
          };

          switch (node.label) {
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
            case "Nuclear Power":
              newNode.data = {
                label: "Nuclear Power",
                icon: Nuclear,
                inputs: [1],
                outputs: [0],
                description: "Provides large-scale base power with low carbon emissions.",
              };
              break;
            case "Coal Power":
              newNode.data = {
                label: "Coal Power",
                icon: Coal,
                inputs: [1],
                outputs: [0],
                description: "Traditional fossil fuel energy source.",
              };
              break;
            case "Solar Power":
              newNode.data = {
                label: "Solar Power",
                icon: Solar,
                inputs: [1],
                outputs: [0],
                description: "Generates renewable energy from sunlight.",
              };
              break;
            case "Wind Power":
              newNode.data = {
                label: "Wind Power",
                icon: Wind,
                inputs: [1],
                outputs: [0],
                description: "Generates renewable energy from wind.",
              };
              break;
            default:
              console.warn(`Unknown label: ${node.label}`);
          }

          return newNode;
        });

        this.edges = edges.map((edge) => ({
          ...edge,
          animated: this.edgeProps.animated,
          style: this.edgeProps.style,
          color: this.edgeProps.color,
        }));



      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Error: ${error.message}`);
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


    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (type === "image") {
        this.imageFile = file;
        if (this.imgUrl) URL.revokeObjectURL(this.imgUrl);
        this.imgUrl = URL.createObjectURL(file);

        // Show alert for JSON upload

        this.$refs.jsonInput.click();
      } else if (type === "json") {
        this.jsonFile = file;
        this.loadScenarioData(); // Handle JSON after image upload
      }
    },

    // Load and parse the JSON file
    loadScenarioData() {
      if (!this.imageFile || !this.jsonFile) {
        console.log('Missing files:', { imageFile: this.imageFile, jsonFile: this.jsonFile });
        alert("Please upload both the image and then the JSON file.");
        return;
      }

      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const data = JSON.parse(e.target.result);
          console.log('Parsed JSON:', data);

          if (!data.nodes || !Array.isArray(data.nodes)) {
            throw new Error("Invalid JSON structure: 'nodes' must be an array.");
          }

          this.nodes = data.nodes.map((node) => {
            const newNode = {
              ...node,
              data: {}, // Will be populated based on label
            };

            switch (node.label) {
              case "Commercial":
                newNode.data = {
                  label: "Commercial",
                  icon: Commercial, // Ensure Commercial is imported or defined
                  inputs: [0],
                  outputs: [0, 1],
                };
                break;
              case "Residential Large":
                newNode.data = {
                  label: "Residential Large",
                  icon: ResidentialLarge, // Ensure ResidentialLarge is imported or defined
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
              case "Nuclear Power":
                newNode.data = {
                  label: "Nuclear Power",
                  icon: Nuclear,
                  inputs: [1],
                  outputs: [0],
                  description: "Provides large-scale base power with low carbon emissions.",
                };
                break;
              case "Coal Power":
                newNode.data = {
                  label: "Coal Power",
                  icon: Coal,
                  inputs: [1],
                  outputs: [0],
                  description: "Traditional fossil fuel energy source.",
                };
                break;
              case "Solar Power":
                newNode.data = {
                  label: "Solar Power",
                  icon: Solar,
                  inputs: [1],
                  outputs: [0],
                  description: "Generates renewable energy from sunlight.",
                };
                break;
              case "Wind Power":
                newNode.data = {
                  label: "Wind Power",
                  icon: Wind,
                  inputs: [1],
                  outputs: [0],
                  description: "Generates renewable energy from wind.",
                };
                break;
              default:
                console.warn(`Unknown label: ${node.label}`);
                newNode.data = {
                  label: "Unknown",
                  icon: null,
                  inputs: [],
                  outputs: [],
                };
            }

            return newNode;
          });

          this.edges = data.edges.map((edge) => ({
            ...edge,
            animated: this.edgeProps.animated,
            style: this.edgeProps.style,
            color: this.edgeProps.color,
          }));



          console.log("Nodes processed:", this.nodes);
          console.log("Edges processed:", this.edges);

        } catch (error) {
          console.error("Error parsing JSON:", error);
          alert(`Invalid JSON file: ${error.message}`);
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
