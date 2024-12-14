<template>
  <Panel id="matrix-container" :header="null">
    <VuePlotly
      :data="data"
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
      data: null,
      layout: null,
    };
  },
  mounted() {
    console.log("init data", this.data);
    this.data = [
      {
        z: this.matrixData,
        x: [0, 1, 2, 3, 4, 5],
        y: [0, 1, 2, 3, 4, 5],
        type: "heatmap",
        hoverongaps: false,
      },
    ];
    this.layout = {
      xaxis: {
        range: [0, 5],
        fixedrange: true,
        scaleanchor: "y",
      },
      yaxis: {
        range: [0, 5],
        fixedrange: true,
        scaleanchor: "x",
      },
      margin: { t: 20, r: 20, b: 40, l: 40 },
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
      this.data = [
        {
          z: newVals,
          x: [0, 1, 2, 3, 4, 5],
          y: [0, 1, 2, 3, 4, 5],
          type: "heatmap",
          hoverongaps: false,
        },
      ];
    },
    resetHeatmap() {
      this.data = [
        {
          z: Array.from({ length: 6 }, () =>
            Array.from({ length: 6 }, () => null)
          ),
          x: [0, 1, 2, 3, 4, 5],
          y: [0, 1, 2, 3, 4, 5],
          type: "heatmap",
          hoverongaps: false,
        },
      ];
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
