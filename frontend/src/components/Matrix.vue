<template>
  <Panel id="matrix-container" :header="null">
    <VuePlotly
      :data="[
        {
          z: z,
          x: axisDimension,
          y: axisDimension,
          xgap: 3,
          ygap: 3,
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
import VueApexCharts from "vue3-apexcharts";
import { VuePlotly } from "vue3-plotly";

export default {
  components: {
    Panel,
    apexchart: VueApexCharts,
    VuePlotly,
  },
  props: {
    matrixData: {
      type: Object,
      required: false,
      default: () => {
        return {
          reset: false,
          autoSimulate: false,
          matrixValues: null,
        };
      },
    },
    matrixTheme: {
      type: String,
      required: false,
      default: "white",
    },
    sliderVals: {
      type: Array,
      required: false,
      default: [0, 0],
    },
  },
  data() {
    return {
      outlinePosition: null,
      z: null,
      layout: null,
      axisDimension: Array.from({ length: 6 }, (_, i) => i),
    };
  },
  mounted() {
    this.z = Array.from({ length: 6 }, (_, rowIndex) =>
      Array.from({ length: 6 }, () => null)
    );
    this.outlinePosition = this.sliderVals;

    this.layout = {
      xaxis: {
        range: [-0.55, 5.55],
        tickmode: "array",
        ticks: "outside",
        showgrid: false,
        zeroline: false,
        gridcolor: "black",
        gridwidth: 5,
        tickvals: [0, 1, 2, 3, 4, 5],
      },
      yaxis: {
        range: [-0.55, 5.55], //-0.5 to 5.5 in order to display the cells with their axis values centered
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
        {
          type: "rect",
          x0: this.outlinePosition[0] - 0.5, // Left boundary of the cell
          x1: this.outlinePosition[0] + 0.48, // Right boundary of the cell
          y0: this.outlinePosition[1] - 0.45, // Bottom boundary of the cell
          y1: this.outlinePosition[1] + 0.45, // Top boundary of the cell
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
    console.log("mounted data", this.data);
  },
  watch: {
    matrixData: {
      handler(newVal) {
        if (newVal && Object.keys(newVal).length > 0) {
          if (!newVal.reset) {
            const colIndex = this.sliderVals[0];
            const rowIndex = this.sliderVals[1];
            this.updateHeatmap(newVal.matrixValues, colIndex, rowIndex);
          } else {
            this.resetHeatmap();
          }
        } else {
          console.error("Not good, matrix is not receiving data");
        }
      },
      deep: true,
    },
    sliderVals: {
      handler(newVal) {
        this.outlinePosition = newVal;
        console.log(this.outlinePosition);
        this.layout = this.layout = {
          ...this.layout, // Spread the existing layout properties
          shapes: [
            {
              ...this.layout.shapes[0],
              x0: this.outlinePosition[0] - 0.5, // Left boundary of the cell
              x1: this.outlinePosition[0] + 0.48, // Right boundary of the cell
              y0: this.outlinePosition[1] - 0.45, // Bottom boundary of the cell
              y1: this.outlinePosition[1] + 0.45, // Top boundary of the cell
            },
          ],
        };

        console.log(this.layout);
      },
    },
    matrixTheme: {
      handler(newVal) {
        this.layout = {
          ...this.layout,
          paper_bgcolor: newVal,
          plot_bgcolor: newVal,
        };
        console.log("Handler worked");
      },
    },
  },
  methods: {
    updateHeatmap(newVals, colIndex, rowIndex) {
      this.z[rowIndex][colIndex] = newVals;
    },
    resetHeatmap() {
      this.z = Array.from({ length: 6 }, () =>
        Array.from({ length: 6 }, () => null)
      );
    },
  },
};
</script>

<style scoped>
.matrix-plotly {
  height: 100%;
  width: 100%;
}
</style>
