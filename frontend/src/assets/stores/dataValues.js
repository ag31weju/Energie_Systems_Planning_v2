import { defineStore } from "pinia";
import { ref } from "vue";

export const useDataStore = defineStore("useDataStore", () => {
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
    colID,
    rowID,
    forMatrix,
    forCharts
  ) {
    function recExtractDataValuesCell(pointer, rec_depth, colIndex, rowIndex) {
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
              let tmp = recExtractDataValuesCell(
                pointer[currColIndex],
                rec_depth + 1,
                currColIndex,
                rowIndex
              );
              console.log("currColIndex", rec_depth, currColIndex, tmp);
              newZ[rowIndex][currColIndex] = tmp
                ? tmp
                : newZ[rowIndex][currColIndex];
            }
          } else if (rec_depth === rowID) {
            for (let currRowIndex = 0; currRowIndex <= 5; currRowIndex++) {
              let tmp = recExtractDataValuesCell(
                pointer[currRowIndex],
                rec_depth + 1,
                colIndex,
                currRowIndex
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
          return recExtractDataValuesCell(
            pointer[capacities[rec_depth]],
            rec_depth + 1,
            colIndex,
            rowIndex
          );
        }
      }
    }

    recExtractDataValuesCell(pointer, 0, 0, 0);
    return;
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
