<template>
  <Panel id="charts-container">
    <div id="chart1-box">
      <div id="chart2-box">
        <Chart
          type="line"
          :data="chartset"
          :options="chartOptions"
          class="h-[30rem]"
          style="height: 10rem; width: 40rem"
        />
      </div>
      <Chart
        type="bar"
        :data="chartset2"
        :options="chartOptions2"
        class="h-[30rem]"
        style="height: 10rem; width: 40rem"
      />
    </div>
  </Panel>
</template>

<script>
import Chart from "primevue/chart";
import Panel from "primevue/panel";
import { ref, watch, onMounted } from "vue";

export default {
  props: {
    chartsData: {
      type: Object,
      required: true,
      default: () => ({}),
    },
    dispatch: {
      type: String,
      required: false,
    },
    time: {
      type: String,
      required: false,
    },
    pv_prodcution: {
      type: String,
      required: false,
    },
    pv_curtailment: {
      type: String,
      required: false,
    },
    purchased_power: {
      type: String,
      required: false,
    },
    demand: {
      type: String,
      required: false,
    },
    storage_charge: {
      type: String,
      required: false,
    },
    storage_discharge: {
      type: String,
      required: false,
    },
  },
  setup(props) {
    const chartset = ref({
      labels: Array.from({ length: 25 }, (_, i) => i),
      datasets: [
        {
          label: "Storage",
          backgroundColor: "rgba(153, 102, 255, 0.2)",
          borderColor: "rgba(153, 102, 255, 1)",
          borderWidth: 1,
          data: [],
        },
      ],
    });

    const chartOptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: "bottom",
        },
      },
    });

    const chartset2 = ref({
      labels: Array.from({ length: 25 }, (_, i) => i),
      datasets: [
        {
          label: "Purchased_Power",
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
        {
          label: "PV Production",
          backgroundColor: "rgba(34, 139, 34, 0.2)",
          borderColor: "rgba(34, 139, 34, 1)",
          borderWidth: 1,
          data: [],
        },
        {
          label: "PV Curtailment",
          backgroundColor: "rgba(255, 255, 0, 0.2)",
          borderColor: "rgba(204, 204, 0, 1)",
          borderWidth: 1,
          data: [],
        },
        {
          label: "Storage Charge",
          backgroundColor: "rgba(255, 165, 0, 0.2)",
          borderColor: "rgba(255, 140, 0, 1)",
          borderWidth: 1,
          data: [],
        },
        {
          label: "Storage Discharge",
          backgroundColor: "rgba(138, 43, 226, 0.2)",
          borderColor: "rgba(75, 0, 130, 1)",
          borderWidth: 1,
          data: [],
        },
      ],
    });

    const chartOptions2 = ref({
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
    });

    function updateChart(data) {
      chartset.value.datasets[0].data = data.lineChartData;
      chartset2.value.datasets[0].data = data.barChartData.purchased_power;
      chartset2.value.datasets[1].data = data.barChartData.demand;
      chartset2.value.datasets[2].data = data.barChartData.pv_prodcution;
      chartset2.value.datasets[3].data = data.barChartData.pv_curtailment;
      chartset2.value.datasets[4].data = data.barChartData.storage_charge;
      chartset2.value.datasets[5].data = data.barChartData.storage_discharge;
    }

    function handleChartsData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        updateChart(newVal);
      } else {
        console.error("Not good, charts are not receiving data");
      }
    }

    watch(
      () => props.chartsData,
      (newVal) => handleChartsData(newVal),
      { deep: true }
    );

    return {
      chartset,
      chartset2,
      chartOptions,
      chartOptions2,
    };
  },
  components: {
    Chart,
    Panel,
  },
  methods: {},
};
</script>

<style>
@import "../assets/main.css";
</style>
