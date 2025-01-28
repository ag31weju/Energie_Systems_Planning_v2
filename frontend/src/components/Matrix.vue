<template>
  <Panel id="matrix-container" :header="null">
    <div id="label-container">
      <label>Node 1</label>
      <label>Node 1</label>
      <label>Node 1</label>
    </div>
    <VuePlotly
      :data="[
        {
          z: z,
          x: matrixDesignStore.axisDimension,
          y: matrixDesignStore.axisDimension,
          type: 'heatmap',
          text:
            z !== null
              ? z.map((row) => row.map((cell) => (cell === null ? '-' : cell)))
              : z,
          texttemplate: '%{text}',
          hoverongaps: false,
          colorscale: 'RdBu',
          zmin: 0,
          zmax: 100,
        },
      ]"
      :layout="matrixDesignStore.layout"
      :display-mode-bar="true"
      :config="{
        displayModeBar: false,
      }"
      class="matrix-plotly"
    ></VuePlotly>
  </Panel>
</template>

<script>
import { Panel } from "primevue";

import ScrollPanel from "primevue/scrollpanel";

import { ref, watch, inject, onMounted, defineExpose } from "vue";
import { VuePlotly } from "vue3-plotly";
import { useDataStore } from "../assets/stores/dataValues";
import { useMatrixDesignStore } from "../assets/stores/matrixDesign";

export default {
  props: {
    matrixData: {
      type: Object,
      required: false,
      default: () => {
        return {
          reset: false,
          matrixValue: null,
        };
      },
    },
    matrixTheme: {
      type: Object,
      required: false,
      default: { backgroundColor: "white", gridColor: "black" },
    },
    sliderVals: {
      type: Array,
      required: false,
      default: [0, 0],
    },
  },
  setup(props) {
    const dataStore = useDataStore();
    const matrixDesignStore = useMatrixDesignStore();

    const z = ref(null);

    function updateHeatmap(newVal, colIndex, rowIndex) {
      z.value[rowIndex][colIndex] = newVal;
    }

    const clearMatrix = () => {
      z.value = Array.from({ length: matrixDesignStore.gridSize }, () =>
        Array.from({ length: matrixDesignStore.gridSize }, () => null)
      );
    };

    onMounted(() => {
      z.value = Array.from(
        { length: matrixDesignStore.gridSize },
        (_, rowIndex) =>
          Array.from({ length: matrixDesignStore.gridSize }, () => null)
      );
      matrixDesignStore.outLinePosition = props.sliderVals;
      matrixDesignStore.initHeatmap();
    });

    function changeMatrix(newVal) {
      if (newVal[0] === -1 || newVal[1] === -1) {
        z.value = Array.from({ length: matrixDesignStore.gridSize }, () =>
          Array.from({ length: matrixDesignStore.gridSize }, () => null)
        );
        return;
      }

      let rowID = dataStore.selectedNodes[1];
      let colID = dataStore.selectedNodes[0];
      const newZ = Array.from({ length: matrixDesignStore.gridSize }, () =>
        Array.from({ length: matrixDesignStore.gridSize }, () => null)
      );

      console.log(dataStore.dataValues);

      dataStore.extractDataValuesCell(
        newZ,
        dataStore.dataValues,
        dataStore.prodCapacities,
        colID,
        rowID,
        true,
        false
      );

      console.log(newZ);

      z.value = newZ;

      matrixDesignStore.handleSliderVals([0, 0]);
    }

    function handleMatrixData(newVal) {
      if (newVal && Object.keys(newVal).length > 0) {
        console.log(newVal.reset);
        if (!newVal.reset) {
          const colIndex = props.sliderVals[0];
          const rowIndex = props.sliderVals[1];
          updateHeatmap(newVal.matrixValue, colIndex, rowIndex);
        } else {
          clearMatrix();
        }
      } else {
        console.error("Not good, matrix is not receiving data");
      }
    }

    //watchers
    watch(
      () => props.matrixData,
      (newVal) => handleMatrixData(newVal),
      { deep: true }
    );
    watch(
      () => props.sliderVals,
      (newVal) => matrixDesignStore.handleSliderVals(newVal),
      { deep: true }
    );
    watch(
      () => props.matrixTheme,
      (newVal) => matrixDesignStore.handleMatrixTheme(newVal),
      { deep: true }
    );

    watch(
      () => dataStore.selectedNodes,
      (newVal) => changeMatrix(newVal),
      {
        deep: true,
      }
    );

    return {
      z,
      clearMatrix,
      matrixDesignStore,
    };
  },
  components: {
    Panel,
    ScrollPanel,
    VuePlotly,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
