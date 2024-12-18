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
          hoverongaps: false,
          colorscale: 'RdBu',
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
      type: Array,
      required: false,
      default: () =>
        Array.from({ length: 6 }, (_, rowIndex) =>
          Array.from({ length: 6 }, () => null)
        ),
    },
    matrixTheme: {
      type: String,
      required: false,
      default: "white",
    },
  },
  data() {
    return {
      z: null,
      layout: null,
      axisDimension: Array.from({ length: 6 }, (_, i) => i),
    };
  },
  mounted() {
    this.z = this.matrixData;

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
          x0: -0.5, // Left boundary of the cell
          x1: 0.5, // Right boundary of the cell
          y0: -0.45, // Bottom boundary of the cell
          y1: 0.45, // Top boundary of the cell
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
          this.updateHeatmap(newVal);
        } else {
          this.resetHeatmap();
        }
      },
      deep: true,
    },
    matrixTheme: {
      handler(newVal) {
        const newLayout = {
          ...this.layout, // Spread existing layout
          paper_bgcolor: newVal,
          plot_bgcolor: newVal,
        };
        this.layout = newLayout;
        console.log("Handler worked");
      },
    },
  },
  methods: {
    updateHeatmap(newVals) {
      this.z = newVals;
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
