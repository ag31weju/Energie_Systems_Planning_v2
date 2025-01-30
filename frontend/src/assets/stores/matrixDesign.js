import { defineStore } from "pinia";
import { ref } from "vue";

export const useMatrixDesignStore = defineStore("useMatrixDesignStore", () => {
  const outLinePosition = ref(null);
  const layout = ref(null);
  const gridSize = ref(6);
  const gridColor = ref("black");
  const gridLines = ref([]);
  const axisDimension = ref(Array.from({ length: 6 }, (_, i) => i));

  function initHeatmap() {
    for (let i = 0; i <= gridSize.value; i++) {
      // Horizontal lines
      gridLines.value.push({
        type: "line",
        x0: -0.5,
        x1: gridSize.value - 0.5,
        y0: i - 0.5,
        y1: i - 0.5,
        line: {
          color: "black",
          width: 1,
        },
      });

      // Vertical lines
      gridLines.value.push({
        type: "line",
        x0: i - 0.5,
        x1: i - 0.5,
        y0: -0.5,
        y1: gridSize.value - 0.5,
        line: {
          color: "black",
          width: 1,
        },
      });
    }

    layout.value = {
      margin: {
        l: 80,

        r: 50,

        b: 50,

        t: 50,
      },
      xaxis: {
        range: [-0.55, gridSize.value - 0.45],
        tickmode: "array",
        ticks: "outside",
        showgrid: false,
        zeroline: false,
        fixedrange: true,
        tickvals: [0, 1, 2, 3, 4, 5],
      },
      yaxis: {
        range: [-0.55, gridSize.value - 0.45], //-0.5 to 5.5 in order to display the cells with their axis values centered
        tickmode: "array",
        ticks: "outside", //for the - at the numbers at the axis baselines
        showgrid: false, //for the grid lines inside the coordinate system
        zeroline: false, //for the baseline of an x axis (the thick one)
        fixedrange: true,
        tickvals: [0, 1, 2, 3, 4, 5], //values where the ticks should be located
      },
      paper_bgcolor: "white", // Background color outside the plotting area
      plot_bgcolor: "white",
      shapes: [
        ...gridLines.value,
        {
          type: "rect",
          x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
          x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
          y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
          y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
          xref: "x",
          yref: "y",
          line: {
            color: "green", // Outline color
            width: 3, // Outline width
          },
          fillcolor: "rgba(0,0,0,0)", // Transparent fill
        },
      ],
    };
  }

  function handleSliderVals(newVal) {
    outLinePosition.value = newVal;

    layout.value = {
      ...layout.value,
      shapes: [
        ...gridLines.value,
        {
          type: "rect",
          x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
          x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
          y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
          y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
          xref: "x",
          yref: "y",
          line: {
            color: "green",
            width: 3,
          },
          fillcolor: "rgba(0,0,0,0)",
        },
      ],
    };
  }

  function handleMatrixTheme(newVal) {
    gridColor.value = newVal.gridColor;
    gridLines.value = [];
    for (let i = 0; i <= gridSize.value; i++) {
      // Horizontal lines
      gridLines.value.push({
        type: "line",
        x0: -0.5,
        x1: gridSize.value - 0.5,
        y0: i - 0.5,
        y1: i - 0.5,
        line: {
          color: newVal.gridColor,
          width: 1,
        },
      });

      // Vertical lines
      gridLines.value.push({
        type: "line",
        x0: i - 0.5,
        x1: i - 0.5,
        y0: -0.5,
        y1: gridSize.value - 0.5,
        line: {
          color: newVal.gridColor,
          width: 1,
        },
      });
    }

    layout.value = {
      ...layout.value,
      paper_bgcolor: newVal.backgroundColor,
      plot_bgcolor: newVal.backgroundColor,
      shapes: [
        ...gridLines.value,
        {
          type: "rect",
          x0: outLinePosition.value[0] - 0.5, // Left boundary of the cell
          x1: outLinePosition.value[0] + 0.48, // Right boundary of the cell
          y0: outLinePosition.value[1] - 0.45, // Bottom boundary of the cell
          y1: outLinePosition.value[1] + 0.45, // Top boundary of the cell
          xref: "x",
          yref: "y",
          line: {
            color: "green",
            width: 3,
          },
          fillcolor: "rgba(0,0,0,0)",
        },
      ],
    };
  }

  return {
    layout,
    outLinePosition,
    axisDimension,
    gridSize,
    initHeatmap,
    handleSliderVals,
    handleMatrixTheme,
  };
});
