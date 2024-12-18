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
      xaxis: {
        range: [-0.55, 5.55],
        tickmode: "array",
        ticks: "",
        gridcolor: "black",
        gridwidth: 5,
        showgrid: false,
        showticklabels: false,
        zeroline: false,
        tickvals: [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], // The positions where the ticks are placed
        ticktext: [0, 1, 2, 3, 4, 5],
      },
      yaxis: {
        range: [-0.55, 5.55], //-0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "", //for the - at the numbers at the axis baselines
        gridcolor: "black",
        gridwidth: 5,
        showgrid: false, //for the grid lines inside the coordinate system
        showticklabels: false,
        zeroline: false, //for the baseline of an x axis (the thick one)
        tickvals: [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5], //values where the ticks should be located
      },
      annotations: [
        //x-axis
        {
          x: 0,
          y: -0.1,
          xref: "x",
          yref: "paper",
          text: "0",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: 1,
          y: -0.1,
          xref: "x",
          yref: "paper",
          text: "1",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: 2,
          y: -0.1,
          xref: "x",
          yref: "paper",
          text: "2",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: 3,
          y: -0.1,
          xref: "x",
          yref: "paper",
          text: "3",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: 4,
          y: -0.1,
          xref: "x",
          yref: "paper",
          text: "4",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: 5,
          y: -0.1,
          xref: "x",
          yref: "paper",
          text: "5",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        //y-axis
        {
          x: -0.05,
          y: 0,
          xref: "paper",
          yref: "y",
          text: "0",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: -0.05,
          y: 1,
          xref: "paper",
          yref: "y",
          text: "1",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: -0.05,
          y: 2,
          xref: "paper",
          yref: "y",
          text: "2",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: -0.05,
          y: 3,
          xref: "paper",
          yref: "y",
          text: "3",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: -0.05,
          y: 4,
          xref: "paper",
          yref: "y",
          text: "4",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
        },
        {
          x: -0.05,
          y: 5,
          xref: "paper",
          yref: "y",
          text: "5",
          showarrow: false,
          font: {
            size: 12,
            color: "black",
          },
          xanchor: "center",
          yanchor: "center",
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
  border-color: black;
  border-width: 3px;
}
</style>
