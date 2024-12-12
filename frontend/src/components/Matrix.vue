<template>
  <Panel id="matrix-container" :header="null">
    <div>
      <apexchart
        type="heatmap"
        height="350"
        style="height: 100%; width: 100%"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </div>
  </Panel>
</template>

<script>
import { Panel } from "primevue";
import VueApexCharts from "vue3-apexcharts";

export default {
  components: {
    Panel,
    apexchart: VueApexCharts,
  },
  props: {
    matrixData: {
      type: Array,
      required: false,
      default: () =>
        Array.from({ length: 6 }, (_, rowIndex) =>
          Array.from({ length: 6 }, () => Math.floor(Math.random() * 100))
        ),
    },
  },
  data() {
    return {
      chartOptions: {
        chart: {
          height: "350",
          type: "heatmap",
        },
        stroke: {
          width: 0,
        },
        plotOptions: {
          heatmap: {
            radius: 30,
            enableShades: false,
            colorScale: {
              ranges: [
                {
                  from: 0,
                  to: 50,
                  color: "#008FFB",
                },
                {
                  from: 51,
                  to: 100,
                  color: "#00E396",
                },
              ],
            },
          },
        },
        dataLabels: {
          enabled: true,
          style: {
            colors: ["#fff"],
          },
        },
        xaxis: {
          type: "category",
        },
        title: {
          text: "Heatmap Example",
        },
      },
      series: this.transformMatrixDataToSeries(),
    };
  },
  watch: {
    matrixData: {
      handler() {
        this.series = this.transformMatrixDataToSeries();
      },
      deep: true,
    },
  },
  methods: {
    transformMatrixDataToSeries() {
      // Convert matrixData into the format ApexCharts expects
      return this.matrixData.map((row, rowIndex) => ({
        name: `Row ${rowIndex + 1}`,
        data: row.map((value, colIndex) => ({
          x: `Col ${colIndex + 1}`,
          y: value,
        })),
      }));
    },
  },
};
</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  height: 100%;
}

th,
td {
  border: 1px solid black;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #f2f2f2;
}
</style>
