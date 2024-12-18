<template>
  <Panel id="matrix-container" :header="null">
    <VuePlotly
      :data="[
        {
          z: z,
          x: axisDimension,
          y: axisDimension,
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
      xaxis: {
        range: [-0.5, 5.5],
        tickmode: "array",
        ticks: "outside",
        showgrid: false,
        zeroline: false,
        tickvals: [0, 1, 2, 3, 4, 5],
      },
      yaxis: {
        range: [-0.5, 5.5], //-0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "outside", //for the - at the numbers at the axis baselines
        showgrid: false, //for the grid lines inside the coordinate system
        zeroline: false, //for the baseline of an x axis (the thick one)
        tickvals: [0, 1, 2, 3, 4, 5], //values where the ticks should be located
      },
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
}
</style>
