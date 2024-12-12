<template>
  <Panel id="charts-container">
    <div id="chart1-box">
      <div id="chart2-box">
        <Chart
          type="line"
          :data="chartset"
          :options="chartOptions"
          class="h-[30rem]"
          style="height: 10rem; width: 50rem"
        />
      </div>
      <Chart
        type="bar"
        :data="chartset2"
        :options="chartOptions2"
        class="h-[30rem]"
        style="height: 10rem; width: 50rem"
      />
    </div>
  </Panel>
</template>

<script>
import Chart from "primevue/chart";
import Panel from "primevue/panel";

export default {
  props: {
    chartsData: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  watch: {
    chartsData: {
      handler(newVal) {
        console.log("ChartsData updated", newVal);
        if (newVal && Object.keys(newVal).length > 0) {
          this.updateChart(newVal);
        } else {
          this.resetChartData();
        }
      },
      deep: true,
    },
  },
  components: {
    Chart,
    Panel,
  },
  data() {
    return {
      // Data for Chart 1
      chartset: {
        labels: Array.from({ length: 25 }, (_, i) => i),
        datasets: [
          {
            label: "Graph A",
            backgroundColor: "rgba(153, 102, 255, 0.2)",
            borderColor: "rgba(153, 102, 255, 1)",
            borderWidth: 1,
            data: [],
          },
        ],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "bottom",
          },
        },
      },
      // Data for Chart 2
      chartset2: {
        labels: Array.from({ length: 25 }, (_, i) => i),
        datasets: [
          {
            label: "Power",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
            data: [],
          },
          {
            label: "Demand",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
            data: [],
          },
        ],
      },
      chartOptions2: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true,
            position: "bottom",
          },
        },
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
      },
    };
  },
  methods: {
    updateChart(data) {
      this.chartset.datasets[0].data = data.lineChartData || [];
      this.chartset2.datasets[0].data = data.barChartData.demand || [];
      this.chartset2.datasets[1].data = data.barChartData.produced || [];
    },
    resetChartData() {
      this.chartset.datasets[0].data = [];
      this.chartset2.datasets.forEach((dataset) => {
        dataset.data = [];
      });
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
