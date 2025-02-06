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
        height: 92%;
        z-index: 2;
      ">
      <vue-flow v-model:nodes="nodes" v-model:edges="edges" :fit-view="true" :zoomOnScroll="false" :zoomOnPinch="false"
        :panOnDrag="false" :pan-on-scroll="false" :disableKeyboardA11y="true" :preventScrolling="true"
        :snap-grid="snapGrid" :snap-to-grid="true" :connection-mode="connectionMode" :node-types="customNodeTypes"
        :auto-pan-on-node-drag="false" :nodes-draggable="locked" :edges-connectable="false" :zoomOnDoubleClick="false"
         :autoPanOnConnect="false" :edgesUpdatable="false" />
    </div>

    <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay1"></canvas>

    <!-- Buttons at the Bottom -->

    <div id="buttons_container">
      <Select v-model="selectedScenario" :options="scenarios" class="Sbutton"
        :placeholder="usedLang.choose_scenario"></Select>

      <Button @click="loadRequest" type="submit" class="button" v-bind:label="usedLang.load_scenario"></Button>
      <Button @click="triggerImageUpload" type="submit" class="button" v-bind:label="usedLang.upload_scenario"></Button>
      <Button @click="triggerJsonUpload" type="submit" class="button" v-bind:label="usedLang.upload_json"></Button>

      <Button @click="toggleGridOverlay" type="submit" class="button" v-bind:label="usedLang.toggle_grid"></Button>
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
import { VueFlow, MarkerType } from "@vue-flow/core";
import "@vue-flow/core/dist/style.css";
import ConsumerNode from "./customNodes/Consumer.vue";
import ProducerNode from "./customNodes/Producer.vue";
import JunctionNode from "./customNodes/Junction.vue";
import BatteryNode from "./customNodes/Battery.vue";

import { getNodeData } from "@/utils/nodeUtils.js";

import { usedLanguage, usedColorBlindnessTheme } from "../assets/stores/pageSettings";
import { ref, reactive, watch } from "vue";
import { useDataStore } from "@/assets/stores/dataValues";
import { useScenarioStore } from "../assets/stores/scenarioStore";

export default {
  inject: ["selectedNodes", "isAutoSimulating", "prepareNewScenario"],
  components: {
    Panel,
    Button,
    VueFlow,
    Select,
  },
  setup(props, context) {
    const usedLang = usedLanguage();
    const currColor = usedColorBlindnessTheme();

    watch(() => currColor.currentColorSettings, () => {
      //   setTimeout(() => {
      //     var root = document.documentElement;
      //     var style = getComputedStyle(root);
      //     var sliderHandleBorder = style.getPropertyValue('--slider-handle-border-color-first').trim();
      //     console.log(`Slider Handle Border Color: ${sliderHandleBorder}`)
      //   })
    })

    watch(() => usedLang.currLang, () => {
      scenarios.value[0] = usedLang.scene_1;
      scenarios.value[1] = usedLang.scene_2;
      scenarios.value[2] = usedLang.scene_3;
    });


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
    const scenarios = ref([usedLang.scene_1, usedLang.scene_2, usedLang.scene_3]); // Scenario options
    const selectedScenario = ref("");

    // Reactive object for edge properties
    const edgeProps = reactive({
      color: "#FA0404", // Edge color
      animated: true, // Edge animation
      style: { stroke: "#FA0404", strokeWidth: 3, opacity: 0.8 }, // Edge style
      type: "bezier",

      markerEnd: { type: MarkerType.Arrow, width: 6, height: 6, color: "#000" },
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
    const optionsConsumer = ref(["Industry", "City", "House"]); // Consumer options

    const selectedProducer = ref(""); // Selected value for producers
    const optionsProducers = ref(["Gas", "Coal", "Solar", "Wind"]); // Producer options

    return {
      usedLang,
      currColor,
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
    async loadRequest() {
      const dataStore = useDataStore();

      if (this.isAutoSimulating) return;

      try {
        const url = "http://127.0.0.1:8000/api/process-scenario/";
        let id = null;
        if (this.selectedScenario == "Scene 1" || this.selectedScenario == "Szene 1") {
          id = 1;
        } else if (this.selectedScenario == "Scene 2" || this.selectedScenario == "Szene 2") {
          id = 2;
        } else if (this.selectedScenario == "Scene 3" || this.selectedScenario == "Szene 3") {
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

        //counts how many prods and cons there are
        dataStore.prodCapacities = new Map();

        this.nodes = nodes.map((node) => {
          if (node.type === "producer" || node.type === "battery")
            dataStore.prodCapacities.set(node.id.at(-1), 0);
          return {
            ...node,
            data: getNodeData(node.label),
          };
        });

        this.edges = edges.map((edge) => ({
          ...edge,
          animated: this.edgeProps.animated,
          style: this.edgeProps.style,
          color: this.edgeProps.color,
        }));

        //new scenario loading finished and assigned each node a prod or cons id
        this.prepareNewScenario();
      } catch (error) {
        console.error("Error fetching data:", error);
        alert(`Error: ${error.message}`);
      }
      this.saveScenario();
    

    },

    async saveScenario() {
    const scenarioStore = useScenarioStore();

    const dataToSave = {
      nodes: this.nodes.map((node) => ({
        id: node.id,
        position: node.position,
        type: node.type,
        label: node.data.label, // Correct access for label
      })),
      edges: this.edges.map((edge) => ({
        id: edge.id,
        source: edge.source,
        target: edge.target,
      
       
      })),
    };

    scenarioStore.saveScenario(dataToSave.nodes, dataToSave.edges);
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

    // Handle file changes for both image and JSON
    triggerImageUpload() {
      if (this.isAutoSimulating) return;
      this.$refs.imageInput.click(); // Trigger image upload
    },
    // Trigger the JSON file input
    triggerJsonUpload() {
      this.nodes = [];
      this.edges = [];
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
    async loadScenarioData() {
      const reader = new FileReader();
      reader.onload = async (e) => {
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
              data: getNodeData(node.label), // Will be populated based on label
            };

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
          this.saveScenario();
      } catch (error) {
        console.error("Error processing JSON:", error);
        alert(`Error: ${error.message}`);
      }
    };

    reader.readAsText(this.jsonFile);
  },
  
}
};
</script>

<style>
@import "../assets/main.css";
</style>
