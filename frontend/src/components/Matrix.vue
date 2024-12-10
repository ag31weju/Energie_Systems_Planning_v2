<template>
  <Panel id="matrix-container">
    <canvas id="chart-matrix"></canvas>
  </Panel>
</template>

<script>
import { Chart, LinearScale } from "chart.js";
import { MatrixController, MatrixElement } from "chartjs-chart-matrix";
import Panel from "primevue/panel";

// Register matrix plugin with Chart.js globally
Chart.register(MatrixController, MatrixElement, LinearScale);

export default {
  props: {
    matrixData: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  data() {
    return {
      matrix: null,
    };
  },
  watch: {
    matrixData: {
      handler(newVal) {
        console.log("MatrixData updated", newVal);
        if (newVal && Object.keys(newVal).length > 0) {
          this.updateMatrix(newVal);
        } else {
          this.resetMatrixData();
        }
      },
      deep: true,
    },
  },
  components: {
    Panel,
    Chart,
    MatrixController,
    MatrixElement,
    LinearScale,
  },
  methods: {
    renderMatrix() {
      const context = document.getElementById("chart-matrix").getContext("2d");
      const initMatrixData = [];

      for (let i = 0; i <= 5; i++) {
        for (let j = 0; j <= 5; j++) {
          initMatrixData.push({
            x: i,
            y: j,
            v: parseInt(`${i}${j}`, 10),
          });
        }
      }

      const initMatrix = {
        datasets: [
          {
            label: "My Matrix",
            data: initMatrixData,
            backgroundColor(context) {
              const value = context.dataset.data[context.dataIndex].v;
              const alpha = (value - 6) / 40 + 0.5;
              return `rgba(0, 128, 0, ${alpha})`;
            },
            borderColor(context) {
              const value = context.dataset.data[context.dataIndex].v;
              const alpha = (value - 6) / 40 + 0.5;
              return `rgba(0, 100, 0, ${alpha})`;
            },
            borderWidth: 1,
            width: ({ chart }) =>
              ((chart.chartArea || {}).width || 0) /
                Math.sqrt(initMatrixData.length) -
              1,
            height: ({ chart }) =>
              ((chart.chartArea || {}).height || 0) /
                Math.sqrt(initMatrixData.length) -
              1,
          },
        ],
      };

      this.matrix = new Chart(context, {
        type: "matrix",
        data: initMatrix,
        options: {
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              callbacks: {
                title() {
                  return "";
                },
                label(context) {
                  const v = context.dataset.data[context.dataIndex];
                  return [`x: ${v.x}`, `y: ${v.y}`, `v: ${v.v}`];
                },
              },
            },
          },
          scales: {
            x: {
              ticks: {
                stepSize: 1,
              },
              grid: {
                display: false,
              },
            },
            y: {
              offset: true,
              ticks: {
                stepSize: 1,
              },
              grid: {
                display: false,
              },
            },
          },
        },
      });
    },
    updateMatrix(data) {
      //only when the matrix exists, should any changes be allowed/Possible
      if (this.matrix) {
        this.matrix.data.datasets[0].data = data;
      }
    },
    resetMatrixData() {
      if (this.matrix) {
        this.matrix.data.datasets[0].data = [];
      }
    },
  },
  mounted() {
    //setTimeout is not a permanent fix
    setTimeout(() => {
      this.renderMatrix();
    }, 100);
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
