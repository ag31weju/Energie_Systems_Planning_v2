<template>
  <Panel id="matrix-container" :header="null">
    <VuePlotly
      :data="[
        {
          z: z,
          x: axisDimension,
          y: axisDimension,
          type: 'heatmap',
          text:
            z !== null
              ? z.map((row) => row.map((cell) => (cell === null ? '-' : cell)))
              : z,
          texttemplate: '%{text}',
          hoverongaps: false,
          colorscale: 'RdBu',
          zmin: -100,
          zmax: 100,
        },
      ]"
      :layout="layout"
      :display-mode-bar="true"
      :config="{
        displayModeBar: true,
        modeBarButtonsToRemove: [
          'zoomIn',
          'zoomOut',
          'zoom',
          'pan2d',
          'resetScale2d',
        ],
      }"
      class="matrix-plotly"
    ></VuePlotly>
  </Panel>
</template>

<script>
import { Panel } from "primevue";
import { ref, watch, inject, onMounted } from "vue";
import VueApexCharts from "vue3-apexcharts";
import { VuePlotly } from "vue3-plotly";

export default {
  props: {
    matrixData: {
      type: Object,
      required: false,
      default: () => {
        return {
          reset: false,
          matrixValue: null,
        };
      },
    },
    matrixTheme: {
      type: Object,
      required: false,
      default: { backgroundColor: "white", gridColor: "black" },
    },
    sliderVals: {
      type: Array,
      required: false,
      default: [0, 0],
    },
  },
  setup(props) {
    const heatmapCollection = [];
    const outLinePosition = ref(null);
    const z = ref(null);
    const layout = ref(null);
    const gridSize = ref(6);
    const gridColor = ref("black");
    const gridLines = ref([]);
    const axisDimension = ref(Array.from({ length: 6 }, (_, i) => i));

    let selectedNodes = inject("selectedNodes");

    function updateHeatmap(newVal, colIndex, rowIndex) {
      z.value[rowIndex][colIndex] = newVal;
    }
    function resetHeatmap() {
      z.value = Array.from({ length: 6 }, () =>
        Array.from({ length: 6 }, () => null)
      );
    }

    function initHeatmap() {
      for (let i = 0; i <= gridSize.value; i++) {
        // Horizontal lines
        gridLines.value.push({
          type: "line",
          x0: -0.5,
          x1: gridSize.value - 0.5,
          y0: i - 0.5,
          y1: i - 0.5,
          line: {
            color: "black",
            width: 1,
          },
        });

        // Vertical lines
        gridLines.value.push({
          type: "line",
          x0: i - 0.5,
          x1: i - 0.5,
          y0: -0.5,
          y1: gridSize.value - 0.5,
          line: {
            color: "black",
            width: 1,
          },
        });
      }

      layout.value = {
        xaxis: {
          range: [-0.55, gridSize.value - 0.45],
          tickmode: "array",
          ticks: "outside",
          showgrid: false,
          zeroline: false,
          gridcolor: "black",
          gridwidth: 5,
          tickvals: [0, 1, 2, 3, 4, 5],
        },
        yaxis: {
          range: [-0.55, gridSize.value - 0.45], //-0.5 to 5.5 in order to display the cells with their axis values centered
          tickmode: "array",
          gridcolor: "black",
          gridwidth: 5,
          ticks: "outside", //for the - at the numbers at the axis baselines
          showgrid: false, //for the grid lines inside the coordinate system
          zeroline: false, //for the baseline of an x axis (the thick one)
          tickvals: [0, 1, 2, 3, 4, 5], //values where the ticks should be located
        },
        paper_bgcolor: "white", // Background color outside the plotting area
        plot_bgcolor: "white",
        shapes: [
          ...gridLines.value,
          {
            type: "rect",
            x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
            x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
            y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
            y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
            xref: "x",
            yref: "y",
            line: {
              color: "green", // Outline color
              width: 3, // Outline width
            },
            fillcolor: "rgba(0,0,0,0)", // Transparent fill
          },
        ],
      };
    }

    onMounted(() => {
      z.value = Array.from({ length: gridSize.value }, (_, rowIndex) =>
        Array.from({ length: gridSize.value }, () => null)
      );
      outLinePosition.value = props.sliderVals;
      initHeatmap();
      heatmapCollection.push({
        selectedNodes: selectedNodes.value,
        z: z.value,
      });
      console.log(heatmapCollection);
    });

    function changeMatrix(newVal) {
      let selectedHeatmap = heatmapCollection.find((el) => {
        const nodeIDs = el.selectedNodes;
        return nodeIDs[0] === newVal[0] && nodeIDs[1] === newVal[1];
      })?.z;

      if (!selectedHeatmap) {
        const newHeatmap = Array.from(
          { length: gridSize.value },
          (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
        );
        selectedHeatmap = newHeatmap;
        heatmapCollection.push({ selectedNodes: newVal, z: selectedHeatmap });
      }

      z.value = selectedHeatmap;

      console.log(heatmapCollection);
      console.log(z.value);
    }

    function handleMatrixData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        if (!newVal.reset) {
          const colIndex = props.sliderVals[0];
          const rowIndex = props.sliderVals[1];
          updateHeatmap(newVal.matrixValue, colIndex, rowIndex);
        } else {
          resetHeatmap();
        }
      } else {
        console.error("Not good, matrix is not receiving data");
      }
      console.log(heatmapCollection);

      /*
      let selectedHeatmap = heatmapCollection.find((el) => {
        const nodeIDs = el.selectedNodes;
        return nodeIDs[0] === 0 && nodeIDs[1] === 1;
      })?.z;

      console.log("z:", selectedHeatmap);

      if (!selectedHeatmap) {
        const newHeatmap = Array.from(
          { length: gridSize.value },
          (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
        );
        selectedHeatmap = newHeatmap;
        heatmapCollection.push({ selectedNodes: [2, 3], z: selectedHeatmap });
      }

      z.value = selectedHeatmap;*/
    }

    function handleSliderVals(newVal) {
      outLinePosition.value = newVal;

      layout.value = {
        ...layout.value,
        shapes: [
          ...gridLines.value,
          {
            type: "rect",
            x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
            x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
            y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
            y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
            xref: "x",
            yref: "y",
            line: {
              color: "green",
              width: 3,
            },
            fillcolor: "rgba(0,0,0,0)",
          },
        ],
      };
    }

    function handleMatrixTheme(newVal) {
      gridColor.value = newVal.gridColor;
      gridLines.value = [];
      for (let i = 0; i <= gridSize.value; i++) {
        // Horizontal lines
        gridLines.value.push({
          type: "line",
          x0: -0.5,
          x1: gridSize.value - 0.5,
          y0: i - 0.5,
          y1: i - 0.5,
          line: {
            color: newVal.gridColor,
            width: 1,
          },
        });

        // Vertical lines
        gridLines.value.push({
          type: "line",
          x0: i - 0.5,
          x1: i - 0.5,
          y0: -0.5,
          y1: gridSize.value - 0.5,
          line: {
            color: newVal.gridColor,
            width: 1,
          },
        });
      }

      layout.value = {
        ...layout.value,
        paper_bgcolor: newVal.backgroundColor,
        plot_bgcolor: newVal.backgroundColor,
        shapes: [
          ...gridLines.value,
          {
            type: "rect",
            x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
            x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
            y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
            y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
            xref: "x",
            yref: "y",
            line: {
              color: "green",
              width: 3,
            },
            fillcolor: "rgba(0,0,0,0)",
          },
        ],
      };
    }

    //watchers
    watch(
      () => props.matrixData,
      (newVal) => handleMatrixData(newVal),
      { deep: true }
    );
    watch(
      () => props.sliderVals,
      (newVal) => handleSliderVals(newVal),
      { deep: true }
    );
    watch(
      () => props.matrixTheme,
      (newVal) => handleMatrixTheme(newVal),
      { deep: true }
    );

    watch(
      () => selectedNodes.value,
      (newVal) => changeMatrix(newVal),
      {
        deep: true,
      }
    );

    return {
      outLinePosition,
      z,
      layout,
      gridSize,
      gridColor,
      gridLines,
      axisDimension,
    };
  },
  components: {
    Panel,
    apexchart: VueApexCharts,
    VuePlotly,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
