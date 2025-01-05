<template>
  <Panel id="charts-container">
    <div id="chart1-box">
      <div id="chart2-box">
        <Chart
          type="line"
          :data="lineChartSet"
          :options="lineChartOptions"
          class="h-[30rem]"
          style="height: 10rem; width: 40rem"
        />
      </div>
      <Chart
        type="bar"
        :data="barChartSet"
        :options="barChartOptions"
        class="h-[30rem]"
        style="height: 10rem; width: 40rem"
      />
    </div>
  </Panel>
</template>

<script>
import Chart from "primevue/chart";
import Panel from "primevue/panel";
import { ref, watch, inject, onMounted } from "vue";
import { usedLanguage } from "../assets/stores/pageSettings";

export default {
  props: {
    chartsData: {
      type: Object,
      required: true,
      default: () => ({}),
    },
    sliderVals: {
      type: Array,
      required: true,
      default: [0, 0],
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
    const chartsCollection = [];

    const usedLang = usedLanguage();
    let selectedNodes = inject("selectedNodes");

    const gridSize = ref(6);

    const lineChartSet = ref({
      labels: Array.from({ length: 25 }, (_, i) => i),
      datasets: [
        {
          label: usedLang.storage_text,
          backgroundColor: "rgba(153, 102, 255, 0.2)",
          borderColor: "rgba(153, 102, 255, 1)",
          borderWidth: 1,
          data: null,
        },
      ],
    });

    const lineChartOptions = ref({
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: true,
          position: "bottom",
        },
      },
    });

    const barChartSet = ref({
      labels: Array.from({ length: 25 }, (_, i) => i),
      datasets: [
        {
          label: usedLang.purchased_power,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
          data: null,
        },
        {
          label: usedLang.demand,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255, 99, 132, 1)",
          borderWidth: 1,
          data: null,
        },
        {
          label: usedLang.pv_production,
          backgroundColor: "rgba(34, 139, 34, 0.2)",
          borderColor: "rgba(34, 139, 34, 1)",
          borderWidth: 1,
          data: null,
        },
        {
          label: usedLang.pv_curtailment,
          backgroundColor: "rgba(255, 255, 0, 0.2)",
          borderColor: "rgba(204, 204, 0, 1)",
          borderWidth: 1,
          data: null,
        },
        {
          label: usedLang.storage_charge,
          backgroundColor: "rgba(255, 165, 0, 0.2)",
          borderColor: "rgba(255, 140, 0, 1)",
          borderWidth: 1,
          data: null,
        },
        {
          label: usedLang.storage_discharge,
          backgroundColor: "rgba(138, 43, 226, 0.2)",
          borderColor: "rgba(75, 0, 130, 1)",
          borderWidth: 1,
          data: null,
        },
      ],
    });

    const barChartOptions = ref({
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

    onMounted(() => {
      chartsCollection.push({
        selectedNodes: selectedNodes.value,
        chartsData: null,
      });

      console.log(chartsCollection);
    });

    function updateChart(newVal, colIndex, rowIndex) {
      assignAllData(newVal);

      console.log(chartsCollection);
    }

    function changeCharts(newVal) {
      let selectedCharts = chartsCollection.find((el) => {
        const nodeIDs = el.selectedNodes;
        return nodeIDs[0] === newVal[0] && nodeIDs[1] === newVal[1];
      })?.chartsData;

      if (!selectedCharts) {
        selectedCharts = null;
        chartsCollection.push({
          selectedNodes: newVal,
          chartsData: selectedCharts,
        });
      }
      assignAllData(selectedCharts[0][0]);

      console.log(chartsCollection);
    }

    function assignAllData(newVal) {
      lineChartSet.value.datasets[0].data = newVal?.lineChartData;
      barChartSet.value.datasets[0].data =
        newVal?.barChartData?.purchased_power;
      barChartSet.value.datasets[1].data = newVal?.barChartData?.demand;
      barChartSet.value.datasets[2].data = newVal?.barChartData?.pv_prodcution;
      barChartSet.value.datasets[3].data = newVal?.barChartData?.pv_curtailment;
      barChartSet.value.datasets[4].data = newVal?.barChartData?.storage_charge;
      barChartSet.value.datasets[5].data =
        newVal?.barChartData?.storage_discharge;
    }

    function handleChartsData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        const colIndex = props.sliderVals[0];
        const rowIndex = props.sliderVals[1];
        updateChart(newVal, colIndex, rowIndex);
      } else {
        console.error("Not good, charts are not receiving data");
      }
    }

    watch(
      () => props.chartsData,
      (newVal) => handleChartsData(newVal),
      { deep: true }
    );

    watch(
      () => selectedNodes.value,
      (newVal) => changeCharts(newVal),
      {
        deep: true,
      }
    );

    return {
      lineChartSet,
      barChartSet,
      lineChartOptions,
      barChartOptions,
    };
  },
  components: {
    Chart,
    Panel,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
