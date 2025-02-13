<template>
  <Panel id="charts-container">
    <Chart
      type="line"
      :data="lineChartSet"
      :options="chartsDesignStore.lineChartOptions"
      class="h-[30rem]"
      style="height: 25vh; width: 45vw"
    />
    <Chart
      type="bar"
      :data="barChartSet"
      :options="chartsDesignStore.barChartOptions"
      class="h-[30rem]"
      style="height: 25vh; width: 45vw"
    />
  </Panel>
</template>

<script>
import Chart from "primevue/chart";
import Panel from "primevue/panel";
import { ref, watch, inject, onMounted, defineExpose } from "vue";
import { usedLanguage } from "../assets/stores/pageSettings";
import { useDataStore } from "../assets/stores/dataValues";
import { useChartsDesignStore } from "../assets/stores/chartsDesign";
export default {
  props: {
    chartsData: {
      type: Object,
      required: true,
      default: () => {
        return {
          reset: false,
          chartsValues: null,
        };
      },
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
    const usedLang = usedLanguage();

    watch(
      () => usedLang.currLang,
      () => {
        lineChartSet.value.datasets[0].label = usedLang.storage_text;
        barChartSet.value.datasets[0].label = usedLang.purchased_power;
        barChartSet.value.datasets[1].label = usedLang.demand;
        barChartSet.value.datasets[2].label = usedLang.pv_production;
        barChartSet.value.datasets[3].label = usedLang.pv_curtailment;
        barChartSet.value.datasets[4].label = usedLang.storage_charge;
        barChartSet.value.datasets[5].label = usedLang.storage_discharge;
      }
    );

    let selectedNodes = inject("selectedNodes");
    const dataStore = useDataStore();
    const chartsDesignStore = useChartsDesignStore();

    const chartsCache = ref(null);

    const gridSize = ref(6);

    const lineChartSet = ref({
      labels: Array.from({ length: 25 }, (_, i) => i),
      datasets: [],
    });

    const barChartSet = ref({
      labels: Array.from({ length: 25 }, (_, i) => i),
      datasets: [],
    });

    onMounted(() => {
      chartsCache.value = Array.from(
        { length: gridSize.value },
        (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
      );
    });

    const clearCharts = () => {
      chartsCache.value = Array.from(
        { length: gridSize.value },
        (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
      );

      barChartSet.value.datasets = [];
      lineChartSet.value.datasets = [];
      Array.from(dataStore.nodeInfo)?.forEach((node, idx) => {
        if (node[1].type !== "junction") {
          barChartSet.value.datasets.push({
            label: node[1].label,
            id: node[0],
            backgroundColor:
              chartsDesignStore.colorValues.background[
                idx % chartsDesignStore.colorValues.background.length
              ],
            borderColor:
              chartsDesignStore.colorValues.border[
                idx % chartsDesignStore.colorValues.border.length
              ],
            borderWidth: 1,
            data: null,
          });
          if (node[1].type === "battery")
            lineChartSet.value.datasets.push({
              label: node[1].label,
              id: node[0],
              backgroundColor: "rgba(153, 102, 255, 0.2)",
              borderColor: "rgba(153, 102, 255, 1)",
              borderWidth: 1,
              data: null,
            });
        }
      });

      assignAllData(null);
    };

    function changeCharts(newVal) {
      if (newVal[0] === -1 || newVal[1] === -1) {
        assignAllData(null);
        chartsCache.value = Array.from(
          { length: gridSize.value },
          (_, rowIndex) => Array.from({ length: gridSize.value }, () => null)
        );
        return;
      }

      let rowID = dataStore.selectedNodes[1];
      let colID = dataStore.selectedNodes[0];
      const newChartsCache = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );

      dataStore.extractDataValuesCell(
        newChartsCache,
        dataStore.dataValues,
        colID,
        rowID,
        false,
        true
      );

      chartsCache.value = newChartsCache;
      assignAllData(
        chartsCache.value[
          dataStore.prodCapacities.get(dataStore.selectedNodes[1])
        ][dataStore.prodCapacities.get(dataStore.selectedNodes[0])]
      );
    }

    function assignAllData(newVal) {
      Array.from(dataStore.nodeInfo).forEach((node) => {
        if (node[1].type !== "junction") {
          let idx = barChartSet.value.datasets.findIndex(
            (dataset) => dataset.id === node[0]
          );
          barChartSet.value.datasets[idx].data = newVal?.barChartData[node[0]];

          if (node[1].type === "battery") {
            let idx = lineChartSet.value.datasets.findIndex(
              (dataset) => dataset.id === node[0]
            );
            console.log("Hello");
            console.log(lineChartSet.value.datasets);
            console.log(newVal?.lineChartData);
            lineChartSet.value.datasets[idx].data =
              newVal?.lineChartData[node[0]];
          }
        }
      });
    }

    function handleChartsData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        if (!newVal.reset) {
          const colIndex = props.sliderVals[0];
          const rowIndex = props.sliderVals[1];
          updateChart(newVal.chartsValues, colIndex, rowIndex);
        } else {
          resetCharts();
        }
      }
    }

    function handleSliderVals(newVal) {
      const rowIndex = newVal[1];
      const colIndex = newVal[0];
      console.log(rowIndex, colIndex);
      console.log(chartsCache.value[rowIndex][colIndex]);
      //assignAllData(chartsCache.value[rowIndex][colIndex]);
    }

    function updateChart(newVal, colIndex, rowIndex) {
      chartsCache.value[rowIndex][colIndex] = newVal;
      assignAllData(newVal);
    }

    function resetCharts() {
      assignAllData(null);
      chartsCache.value = Array.from({ length: gridSize.value }, () =>
        Array.from({ length: gridSize.value }, () => null)
      );
    }

    watch(
      () => props.chartsData,
      (newVal) => handleChartsData(newVal),
      { deep: true }
    );

    watch(
      () => props.sliderVals,
      (newVal) => handleSliderVals(newVal),
      { deep: true }
    );

    watch(
      () => dataStore.selectedNodes,
      (newVal) => changeCharts(newVal),
      {
        deep: true,
      }
    );

    return {
      lineChartSet,
      barChartSet,
      chartsDesignStore,
      usedLang,
      clearCharts,
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
