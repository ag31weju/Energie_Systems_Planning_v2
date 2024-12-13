<template>
    <Panel id="playfield">
        <!-- Image Box -->
        <div id="image_box" style="position: relative;">
            <!-- Display Image -->
            <img :src="imgUrl" style="max-width: 100%; max-height: auto; object-fit: contain;" ref="imageElement" />

            <!-- Canvas for Grid Overlay -->
            <canvas v-if="showGrid" ref="gridCanvas" id="grid_overlay"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1;"></canvas>

            <!-- Sigma.js Container -->
            <div ref="sigmaContainer" id="sigma_overlay"
                style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; pointer-events: auto; z-index: 1;">
            </div>
        </div>

        <!-- Buttons at the Bottom -->
        <div id="buttons_container">
            <Button @click="loadRequest" type="submit" class="slider-button">Load Scenario</Button>
            <Button @click="initSigma" type="submit" class="slider-button">Toggle Grid</Button>
            <Button @click="triggerFileUpload" type="button" class="slider-button">Upload Scenario</Button>
        </div>

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
    data() {
        return {
            imgUrl: null, // URL for the image
            showGrid: false, // Flag for showing grid
            gridSize: 15, // Grid size (number of cells per row/column)

            imageFile: null, // To store selected image
            jsonFile: null, // To store selected JSON file

            sigmaInstance: null, // Reference to the Sigma.js instance
        };
    },
    components: {
        Panel,
        Button,
    },
    methods: {

        initSigma() {
            const graph = new Graph();

            // Get image and canvas dimensions
            const imgElement = this.$refs.imageElement;
            const width = imgElement.offsetWidth;
            const height = imgElement.offsetHeight;

            const gridSize = this.gridSize;
            const cellWidth = width / 15;
            const cellHeight = height / 15;

            // Define your nodes with grid-based coordinates
            const nodes = [
                { id: "node1", gridX: 0, gridY: 0, label: "A", color: "#FF0000" },
                { id: "node2", gridX: 5, gridY: 5, label: "B", color: "#00FF00" },
                { id: "node3", gridX: 9, gridY: 10, label: "C", color: "#0000FF" },
                { id: "node4", gridX: 2, gridY: 2, label: "D", color: "#FF0000" },
                { id: "node5", gridX: 1, gridY: 8, label: "E", color: "#00FF00" },
                { id: "node6", gridX: 1, gridY: 5, label: "F", color: "#0000FF" },
            ];

            // Add nodes to the graph
            nodes.forEach((node) => {
                const nodeX = node.gridX * cellWidth;
                const nodeY = node.gridY * cellHeight;

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
            this.sigmaInstance = new Sigma(graph, container, {
                enablePan: false, // Disable panning
                enableZoom: false, // Enable zoom
                enableEdgeHoverEvents: true, // Enable edge hover events
                enableCameraPanning: false,
                enableCameraZooming: false,
            });


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





        async loadRequest() {
            try {
                const url = "http://127.0.0.1:8000/api/process-scenario/";
                const id = 1;

                const imgResponse = await axios.get(url, {
                    params: { id, filetype: "png" },
                    responseType: "blob",
                });

                if (this.imgUrl) {
                    URL.revokeObjectURL(this.imgUrl);
                }

                this.imgUrl = URL.createObjectURL(imgResponse.data);

                const imgElement = this.$refs.imageElement;
                imgElement.onload = () => {
                    this.initSigma();
                    // Disable panning (dragging) by modifying the camera settings
                    this.sigmaInstance.getMouseCaptor().setState("disabled");
                    this.sigmaInstance.getMouseCaptor().disable();

                };
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
                this.$nextTick(() => {
                    if (oldUrl) {
                        setTimeout(() => URL.revokeObjectURL(oldUrl), 1000);
                    }
                    this.initSigma();
                });
                alert("Image & Json successfully processed and updated!");

            } catch (error) {
                console.error("Error uploading files:", error);
                alert("Failed to upload files. Please try again.");
            }
        },


        //End---Scenario Upload------//
    },

    mounted() {
        if (this.imgUrl) {
            this.initSigma();
        }
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

#image_box {
    position: absolute;
    top: 0;
    /* Anchor to the bottom of the parent */
    left: 0;
    width: 100%;
    height: 90%;
    /* Default height */
    background-color: #f4f4f4;
    overflow: hidden;
    transition: height 0.3s ease;
    /* Smoothly animate height changes */
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
}

.slider-button {
    margin-bottom: 5px;
    /* Reduced space between buttons */
}

#sigma_overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    /* Ensure it matches the image width */
    height: 100%;
    /* Ensure it matches the image height */
    pointer-events: none;
    z-index: 2;
    /* Ensure it renders above other elements */
}
</style>