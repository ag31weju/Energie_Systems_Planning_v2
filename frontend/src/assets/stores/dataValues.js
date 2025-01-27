import { defineStore } from "pinia";
import { ref } from "vue";

export const usedDataStore = defineStore("usedDataStore", () => {
  const selectedNodes = ref([-1, -1]);
  const dataValues = ref(undefined);
  const prodCapacities = ref(undefined);

  function getDataValuesCell(pointer) {
    for (let i = 0; i < prodCapacities.value.length; i++) {
      if (i === prodCapacities.value.length - 1) {
        return pointer[prodCapacities.value[i]];
      }

      if (!pointer) {
        console.error("prodCapacities length is not equal to dataValues depth");
        throw new Error(
          "prodCapacities length is not equal to dataValues depth"
        );
      }

      pointer = pointer[prodCapacities.value[i]];
    }
  }

  function extractDataValuesCell(
    newZ,
    pointer,
    capacities,
    rec_depth,
    colID,
    rowID,
    colIndex,
    rowIndex,
    forMatrix,
    forCharts
  ) {
    if (rec_depth == capacities.length) {
      return forMatrix
        ? pointer.matrixData
        : forCharts
        ? pointer.chartsData
        : console.error("data cannot be assigned to visualization component");
    } else {
      if (selectedNodes.value.some((el) => el === rec_depth)) {
        if (rec_depth === colID) {
          for (let currColIndex = 0; currColIndex <= 5; currColIndex++) {
            let tmp = extractDataValuesCell(
              newZ,
              pointer[currColIndex],
              capacities,
              rec_depth + 1,
              colID,
              rowID,
              currColIndex,
              rowIndex,
              forMatrix,
              forCharts
            );
            console.log("currColIndex", rec_depth, currColIndex, tmp);
            newZ[rowIndex][currColIndex] = tmp
              ? tmp
              : newZ[rowIndex][currColIndex];
          }
        } else if (rec_depth === rowID) {
          for (let currRowIndex = 0; currRowIndex <= 5; currRowIndex++) {
            let tmp = extractDataValuesCell(
              newZ,
              pointer[currRowIndex],
              capacities,
              rec_depth + 1,
              colID,
              rowID,
              colIndex,
              currRowIndex,
              forMatrix,
              forCharts
            );
            console.log("currRowIndex", rec_depth, currRowIndex, tmp);
            newZ[currRowIndex][colIndex] = tmp
              ? tmp
              : newZ[currRowIndex][colIndex];
          }
        } else {
          console.error("rec_depth does not equal any selected node ID");
        }
      } else {
        console.log("hello", rec_depth);
        return extractDataValuesCell(
          newZ,
          pointer[capacities[rec_depth]],
          capacities,
          rec_depth + 1,
          colID,
          rowID,
          colIndex,
          rowIndex,
          forMatrix,
          forCharts
        );
      }
    }
  }

  function updateDataValuesCell(pointer, propagateChange) {
    for (let i = 0; i < prodCapacities.value.length; i++) {
      if (i === prodCapacities.value.length - 1) {
        pointer[prodCapacities.value[i]] = propagateChange.simData;
        return;
      }

      if (!pointer) {
        console.error("prodCapacities length is not equal to dataValues depth");
        throw new Error(
          "prodCapacities length is not equal to dataValues depth"
        );
      }

      pointer = pointer[prodCapacities.value[i]];
    }
  }

  return {
    dataValues,
    prodCapacities,
    selectedNodes,
    getDataValuesCell,
    updateDataValuesCell,
    extractDataValuesCell,
  };
});
