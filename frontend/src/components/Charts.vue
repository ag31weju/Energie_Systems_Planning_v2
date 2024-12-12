<template>
  <Panel id="charts-container">
    <div id="chart1-box">
      <Chart
        type="bar"
        :data="chartset"
        :options="chartOptions"
        class="h-[30rem]"
        style="height: 10rem; width: 50rem"
      />
    </div>
    <div id="chart2-box">
      <Chart
        type="line"
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
  props: [
    "dispatch",
    "time",
    "pv_production",
    "pv_curtailment",
    "purchased_power",
    'demand',
    'storage_charge',
    'storage_discharge',
  ],
  components: {
    Chart,
    Panel,
  },
  data() {
    return {
      // Data for Chart 1
      chartset: {
        labels: ["January", "February", "March", "April", "May", "June"],
        datasets: [
          {
            label: "Graph 1",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            borderColor: "rgba(75, 192, 192, 1)",
            borderWidth: 1,
            data: [65, 59, 80, 81, 56, 55],
          },
          {
            label: "Graph 2",
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
            data: [28, 48, 40, 19, 86, 27],
          },
          {
            label: "Graph 4",
          },
          {
            label: "Graph 5",
          },
          {
            label: "Graph 6",
          },
          {
            label: "Graph 7",
          },
          {
            label: "Graph 8",
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
        scales: {
          x: {
            stacked: true,
          },
          y: {
            stacked: true,
          },
        },
      },
      // Data for Chart 2
      chartset2: {
        labels: [
          "July",
          "August",
          "September",
          "October",
          "November",
          "December",
        ],
        datasets: [
          {
            label: "Graph A",
            backgroundColor: "rgba(153, 102, 255, 0.2)",
            borderColor: "rgba(153, 102, 255, 1)",
            borderWidth: 1,
            data: [45, 67, 75, 50, 40, 90],
          },
          {
            label: "Graph B",
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
            data: [30, 40, 55, 70, 60, 80],
          },
          {
            label: "Graph C",
          },
          {
            label: "Graph D",
          },
          {
            label: "Graph E",
          },
          {
            label: "Graph F",
          },
          {
            label: "Graph G",
          },
          {
            label: "Graph H",
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
      },
    };
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
