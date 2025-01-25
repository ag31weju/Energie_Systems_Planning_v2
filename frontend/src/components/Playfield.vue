<template>
  <Panel id="playfield">
    <!-- Image Box -->

    <!-- Vue Flow Container -->
    <div id="vueflow_container" ref="vueFlowContainer" :style="{
      backgroundImage: 'url(' + imgUrl + ')',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
    }" style="
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 43.5rem;
        z-index: 2;
      ">
      <vue-flow v-model:nodes="nodes" v-model:edges="edges" :fit-view="true" :zoomOnScroll="false" :zoomOnPinch="false"
        :panOnDrag="false" :pan-on-scroll="false" :preventScrolling="true" :snap-grid="snapGrid" :snap-to-grid="true"
        :coordinateExtent="coordinateExtent" :connection-mode="connectionMode" :node-types="customNodeTypes"
        :auto-pan-on-node-drag="false" :nodes-draggable="!locked" :edges-connectable="edgeMode"
        :zoomOnDoubleClick="false" @connect="onConnect" />
    </div>

    <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay"></canvas>

    <!-- Buttons at the Bottom -->
    <div id="buttons_container1">
      <!-- Dropdowns -->

      <!-- Scenario Management -->
      <div class="row">
        <Select v-model="selectedScenario" :options="scenarios" class="Sbutton" placeholder="Choose Scenario"></Select>
        <Button @click="loadRequest" type="submit" class="button" v-bind:label="usedLang.load_scenario"></Button>
        <Button @click="triggerJsonUpload" type="submit" class="slider-button" v-bind:label="upload_json">json</Button>
        <Button @click="triggerImageUpload" type="submit" class="button"
          v-bind:label="usedLang.upload_scenario">img</Button>

        <Button @click="toggleGridOverlay" type="submit" class="button" v-bind:label="usedLang.toggle_grid"></Button>
        <Button @click="clearNodes" type="submit" class="button" v-bind:label="usedLang.clear_nodes"></Button>
        <Button @click="saveData" type="submit" class="button" v-bind:label="usedLang.save_text"></Button>
      </div>
      <!-- Utilities -->
      <div class="row">
        <Button @click="toggleEdgeMode" type="submit" class="button" v-bind:label="usedLang.add_edge"></Button>

        <Button @click="addConsumerNode" type="submit" class="button" v-bind:label="usedLang.add_consumer"></Button>
        <Button @click="addBatteryNode" type="submit" class="button">Add Battery</Button>
        <Button @click="addJunctionNode" type="submit" class="button">Add Junction</Button>
        <Button @click="addEnergySourceNode" type="submit" class="button"
          v-bind:label="usedLang.add_energy_source"></Button>
      </div>
      <!-- Actions -->

      <div class="row">
        <Select v-model="selectedConsumer" :options="optionsConsumer"
          :placeholder="usedLang.selector_text_consumer"></Select>
        <Select v-model="selectedProducer" :options="optionsProducers"
          :placeholder="usedLang.selector_text_producer"></Select>
      </div>
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
import BatteryNode from "./customNodes/Battery.vue";
import JunctionNode from "./customNodes/Junction.vue";
import ProducerNode from "./customNodes/Producer.vue";

import Industry from "@/assets/node_images/consumer/Industry.png";
import City from "@/assets/node_images/consumer/City.png";
import House from "@/assets/node_images/consumer/House.png";

import Battery from "@/assets/node_images/misc/battery.png";
import Junction from "@/assets/node_images/misc/junction.png";

import Gas from "@/assets/node_images/producer/Gas.png";
import Coal from "@/assets/node_images/producer/Coal.png";
import Solar from "@/assets/node_images/producer/Solar.png";
import Wind from "@/assets/node_images/producer/Wind.png";

import { usedLanguage } from "../assets/stores/pageSettings";
import { inject, ref, reactive } from "vue";

export default {
  components: {
    Panel,
    Button,
    Select,
    VueFlow,
  },
  setup() {
    const usedLang = usedLanguage();

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
      battery: BatteryNode,
      junction: JunctionNode,
    });

    // Reactive state for selected consumer/producer and their options
    const selectedConsumer = ref(""); // Selected value for consumers
    const optionsConsumer = ref(["Industry", "City", "House"]);
    const selectedProducer = ref(""); // Selected value for producers
    const optionsProducers = ref(["Gas", "Coal", "Solar", "Wind"]); // Producer options
    const scenarios = ref(["Scene 1", "Scene 2", "Scene 3"]); // Scenario options
    const selectedScenario = ref("");

    return {
      usedLang,
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
      scenarios,
      selectedScenario,
    };
  },

  methods: {
    toggleLock() {
      this.locked = !this.locked;
    },
    async loadRequest() {
      try {
        const url = "http://127.0.0.1:8000/api/process-scenario/";
        let id = null;
        if (this.selectedScenario == "Scene 1") {
          id = 1;
        } else if (this.selectedScenario == "Scene 2") {
          id = 2;
        } else if (this.selectedScenario == "Scene 3") {
          id = 3;
        }

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
            case "Industry":
              newNode.data = {
                label: "Industry",
                icon: Industry,
                inputs: [0, 1],
                outputs: [2, 3],
              };
              break;
            case "City":
              newNode.data = {
                label: "City",
                icon: City,
                inputs: [0, 1],
                outputs: [2, 3],
              };
              break;
            case "House":
              newNode.data = {
                label: "House",
                icon: ResidentialSmall,
                inputs: [0, 1],
                outputs: [2, 3],
              };
              break;
            case "Gas":
              newNode.data = {
                label: "Gas",
                icon: Gas,
                inputs: [0, 1],
                outputs: [2, 3],
                description:
                  "Provides large-scale base power with low carbon emissions.",
              };
              break;
            case "Coal":
              newNode.data = {
                label: "Coal",
                icon: Coal,
                inputs: [0, 1],
                outputs: [2, 3],
                description: "Traditional fossil fuel energy source.",
              };
              break;
            case "Solar":
              newNode.data = {
                label: "Solar",
                icon: Solar,
                inputs: [0, 1],
                outputs: [2, 3],
                description: "Generates renewable energy from sunlight.",
              };
              break;
            case "Wind":
              newNode.data = {
                label: "Wind",
                icon: Wind,
                inputs: [0, 1],
                outputs: [2, 3],
                description: "Generates renewable energy from wind.",
              };
              break;
              case "Battery":
  newNode.data = {
    label: "Battery",
    icon: Battery, 
    inputs: [0, 1], 
    outputs: [2, 3], 
    description: "Stores energy for later use and provides backup power.",
  };
  break;

case "Junction":
  newNode.data = {
    label: "Junction",
    icon: Junction, 
    inputs: [0, 1,], 
    outputs: [2, 3], 
    description: "Connects and distributes inputs to various outputs.",
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

    addBatteryNode() {
      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth / this.gridSize;
      const height = vueFlowContainer.offsetHeight / this.gridSize;

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "battery",
        position: { x: width * 5, y: height * 3 },
        data: {
          label: "Battery",
          icon: Battery,
          inputs: [0, 1],
          outputs: [2, 3],
        },

      };
      this.nodes.push(newNode);
    },

    addJunctionNode() {
      const vueFlowContainer = this.$refs.vueFlowContainer;
      if (!vueFlowContainer) return;

      const width = vueFlowContainer.offsetWidth / this.gridSize;
      const height = vueFlowContainer.offsetHeight / this.gridSize;

      const newNode = {
        id: `node_${this.nodeIdCounter++}`,
        type: "junction",
        position: { x: width * 7, y: height * 3 },
        data: {
          label: "Junction",
          icon: Junction,
          inputs: [0, 1],
          outputs: [2, 3],
        },
      };
      this.nodes.push(newNode);
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
        case "Gas":
          newNode.data = {
            label: "Gas",
            icon: Gas, // Add an icon path if available
            inputs: [0, 1],
            outputs: [2, 3],
            description:
              "Provides large-scale base power with low carbon emissions.",
          };
          break;

        case "Coal":
          newNode.data = {
            label: "Coal",
            icon: Coal, // Add an icon path if available
            inputs: [0, 1],
          outputs: [2, 3],
            description: "Traditional fossil fuel energy source.",
          };
          break;

        case "Solar":
          newNode.data = {
            label: "Solar",
            icon: Solar, // Add an icon path if available
            inputs: [0, 1],
          outputs: [2, 3],
            description: "Generates renewable energy from sunlight.",
          };
          break;

        case "Wind":
          newNode.data = {
            label: "Wind",
            icon: Wind, // Add an icon path if available
            inputs: [0, 1],
          outputs: [2, 3],
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
        case "Industry":
          newNode.data = {
            label: "Industry",
            icon: Industry,
            inputs: [0, 1],
          outputs: [2, 3],
          };
          break;

        case "City":
          newNode.data = {
            label: "City",
            icon: City,
            inputs: [0, 1],
          outputs: [2, 3],
          };
          break;

        case "House":
          newNode.data = {
            label: "House",
            icon: ResidentialSmall,
            inputs: [0, 1],
          outputs: [2, 3],
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
          sourceHandle: connection.sourceHandle, // Ensure correct handle connection
          targetHandle: connection.targetHandle, // Ensure correct handle connection
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
            sourceHandle:edge.sourceHandle,
            targetHandle: edge.targetHandle,

          })),
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
          alert("Graph Data downloaded successfully");
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

   
        
      } catch (error) {
        console.error("Error saving data:", error);
        alert(`Error: ${error.message}`);
      }
    },

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
      const reader = new FileReader();
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result);

          // Check for both JSON structures
          const nodes = json.nodes || json.data.nodes;
          const edges = json.edges || json.data.edges;

          if (!nodes || !Array.isArray(nodes)) {
            throw new Error(
              "Invalid JSON structure: 'nodes' must be an array."
            );
          }

          if (!edges || !Array.isArray(edges)) {
            throw new Error(
              "Invalid JSON structure: 'edges' must be an array."
            );
          }

          this.nodes = nodes.map((node) => {
            const newNode = {
              ...node,
              data: {}, // Will be populated based on label
            };

            switch (node.label) {
              case "Industry":
                newNode.data = {
                  label: "Industry",
                  icon: Industry, // Ensure Industry is imported or defined
                  inputs: [0, 1],
                  outputs: [2, 3],
                };
                break;
              case "City":
                newNode.data = {
                  label: "City",
                  icon: City, // Ensure City is imported or defined
                  inputs: [0, 1],
                  outputs: [2, 3],
                };
                break;
              case "House":
                newNode.data = {
                  label: "House",
                  icon: ResidentialSmall,
                  inputs: [0, 1],
                  outputs: [2, 3],
                };
                break;
              case "Gas":
                newNode.data = {
                  label: "Gas",
                  icon: Gas,
                  inputs: [0, 1],
                  outputs: [2, 3],
                  description:
                    "Provides large-scale base power with low carbon emissions.",
                };
                break;
              case "Coal":
                newNode.data = {
                  label: "Coal",
                  icon: Coal,
                  inputs: [0, 1],
                  outputs: [2, 3],
                  description: "Traditional fossil fuel energy source.",
                };
                break;
              case "Solar":
                newNode.data = {
                  label: "Solar",
                  icon: Solar,
                  inputs: [0, 1],
                  outputs: [2, 3],
                  description: "Generates renewable energy from sunlight.",
                };
                break;
              case "Wind":
                newNode.data = {
                  label: "Wind Power",
                  icon: Wind,
                  inputs: [0, 1],
                  outputs: [2, 3],
                  description: "Generates renewable energy from wind.",
                };
                break;
                case "Battery":
  newNode.data = {
    label: "Battery",
    icon: Battery, 
    inputs: [0, 1], 
    outputs: [2, 3], 
    description: "Stores energy for later use and provides backup power.",
  };
  break;

case "Junction":
  newNode.data = {
    label: "Junction",
    icon: Junction, 
    inputs: [0, 1,], 
    outputs: [2, 3], 
    description: "Connects and distributes inputs to various outputs.",
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

          this.edges = edges.map((edge) => ({
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
@import "../assets/main.css";
</style>
