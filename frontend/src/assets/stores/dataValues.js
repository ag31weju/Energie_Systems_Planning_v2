import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useDataStore = defineStore("useDataStore", () => {
  const selectedNodes = ref([-1, -1]);
  const dataValues = ref(null);
  const prodCapacities = ref(new Map());

  const isSelectedFirst = (nodeID) => {
    return selectedNodes.value ? selectedNodes.value[0] === nodeID : false;
  };
  const isSelectedSecond = (nodeID) => {
    return selectedNodes.value ? selectedNodes.value[1] === nodeID : false;
  };

  function getDataValuesCell(pointer) {
    const prodCapacitiesArr = Array.from(prodCapacities.value);
    for (let i = 0; i < prodCapacitiesArr.length; i++) {
      if (i === prodCapacitiesArr.length - 1) {
        return pointer[prodCapacitiesArr[i][1]];
      }

      if (!pointer) {
        console.error("prodCapacities length is not equal to dataValues depth");
        throw new Error(
          "prodCapacities length is not equal to dataValues depth"
        );
      }

      pointer = pointer[prodCapacitiesArr[i][1]];
    }
  }

  function extractDataValuesCell(
    matrixToWhichIsAssigned,
    pointer,
    colID,
    rowID,
    forMatrix,
    forCharts
  ) {
    console.log(colID);
    console.log(rowID);
    const prodCapacitiesArr = Array.from(prodCapacities.value);
    function recExtractDataValuesCell(pointer, rec_depth, colIndex, rowIndex) {
      if (rec_depth == prodCapacitiesArr.length) {
        return forMatrix
          ? pointer.matrixData
          : forCharts
          ? pointer.chartsData
          : console.error("data cannot be assigned to visualization component");
      } else {
        if (
          selectedNodes.value.some(
            (el) => el === prodCapacitiesArr[rec_depth][0]
          )
        ) {
          if (prodCapacitiesArr[rec_depth][0] == colID) {
            for (let currColIndex = 0; currColIndex <= 5; currColIndex++) {
              let tmp = recExtractDataValuesCell(
                pointer[currColIndex],
                rec_depth + 1,
                currColIndex,
                rowIndex
              );
              console.log("for columns", colID, currColIndex, tmp);
              matrixToWhichIsAssigned[rowIndex][currColIndex] =
                tmp !== null && tmp !== undefined
                  ? tmp
                  : matrixToWhichIsAssigned[rowIndex][currColIndex];
            }
          } else if (prodCapacitiesArr[rec_depth][0] == rowID) {
            for (let currRowIndex = 0; currRowIndex <= 5; currRowIndex++) {
              let tmp = recExtractDataValuesCell(
                pointer[currRowIndex],
                rec_depth + 1,
                colIndex,
                currRowIndex
              );
              console.log("for rows", rowID, currRowIndex, tmp);
              matrixToWhichIsAssigned[currRowIndex][colIndex] =
                tmp !== null && tmp !== undefined
                  ? tmp
                  : matrixToWhichIsAssigned[currRowIndex][colIndex];
            }
          } else {
            console.error("rec_depth does not equal any selected node ID");
          }
        } else {
          return recExtractDataValuesCell(
            pointer[prodCapacitiesArr[rec_depth][1]],
            rec_depth + 1,
            colIndex,
            rowIndex
          );
        }
      }
    }

    return recExtractDataValuesCell(pointer, 0, 0, 0);
  }

  function updateDataValuesCell(pointer, propagateChange) {
    const prodCapacitiesArr = Array.from(prodCapacities.value);
    for (let i = 0; i < prodCapacitiesArr.length; i++) {
      if (i === prodCapacitiesArr.length - 1) {
        pointer[prodCapacitiesArr[i][1]] = propagateChange.simData;

        return;
      }

      if (!pointer) {
        console.error("prodCapacities length is not equal to dataValues depth");
        throw new Error(
          "prodCapacities length is not equal to dataValues depth"
        );
      }

      pointer = pointer[prodCapacitiesArr[i][1]];
    }
  }

  return {
    dataValues,
    prodCapacities,
    selectedNodes,
    isSelectedFirst,
    isSelectedSecond,
    getDataValuesCell,
    updateDataValuesCell,
    extractDataValuesCell,
  };
});
