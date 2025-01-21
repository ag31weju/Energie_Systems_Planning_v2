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
          zmin: 0,
          zmax: 100,
        },
      ]"
      :layout="layout"
      :display-mode-bar="true"
      :config="{
        displayModeBar: false,
        /*displaylogo: false,
        modeBarButtonsToRemove: [
          'zoomIn',
          'zoomOut',
          'zoom',
          'pan2d',
          'resetScale2d',
          'toImage',
        ],*/
      }"
      class="matrix-plotly"
    ></VuePlotly>
  </Panel>
</template>

<script>
import { Panel } from "primevue";
import { ref, watch, inject, onMounted, defineExpose } from "vue";
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
    const outLinePosition = ref(null);
    const z = ref(null);
    const layout = ref(null);
    const gridSize = ref(6);
    const gridColor = ref("black");
    const gridLines = ref([]);
    const axisDimension = ref(Array.from({ length: 6 }, (_, i) => i));

    let selectedNodes = inject("selectedNodes");
    let prodCapacities = inject("prodCapacities");
    let dataValues = inject("dataValues");
    let extractDataValuesCell = inject("extractDataValuesCell");

    function updateHeatmap(newVal, colIndex, rowIndex) {
      z.value[rowIndex][colIndex] = newVal;
    }
    function resetHeatmap() {
      z.value = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );
    }

    const clearMatrix = () => {
      z.value = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );
    };

    defineExpose({ clearMatrix });

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
          fixedrange: true,
          tickvals: [0, 1, 2, 3, 4, 5],
        },
        yaxis: {
          range: [-0.55, gridSize.value - 0.45], //-0.5 to 5.5 in order to display the cells with their axis values centered
          tickmode: "array",
          ticks: "outside", //for the - at the numbers at the axis baselines
          showgrid: false, //for the grid lines inside the coordinate system
          zeroline: false, //for the baseline of an x axis (the thick one)
          fixedrange: true,
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
    });

    function changeMatrix(newVal) {
      if (newVal[0] === -1 || newVal[1] === -1) {
        z.value = Array.from({ length: gridSize.value }, () =>
          Array.from({ length: gridSize.value }, () => null)
        );
        return;
      }

      let rowID = selectedNodes.value[1];
      let colID = selectedNodes.value[0];
      const newZ = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );

      console.log(dataValues.value);

      extractDataValuesCell(
        newZ,
        dataValues.value,
        prodCapacities.value,
        0,
        colID,
        rowID,
        0,
        0,
        true,
        false
      );

      /*let selectedHeatmap = heatmapCollection.find((el) => {
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
      }*/

      z.value = newZ;

      handleSliderVals([0, 0]);
    }

    function handleMatrixData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        console.log(newVal.reset);
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
      clearMatrix,
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
