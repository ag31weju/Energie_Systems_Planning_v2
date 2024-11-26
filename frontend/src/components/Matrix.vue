<template>
  <div>
    <canvas id="chart-matrix"></canvas>
  </div>
</template>

<script>
import { Chart, LinearScale } from "chart.js";
import { MatrixController, MatrixElement } from "chartjs-chart-matrix";

// Register matrix plugin with Chart.js globally
Chart.register(MatrixController, MatrixElement, LinearScale);

export default {
  data() {
    return {
      matrix: null,
    };
  },
  methods: {
    renderMatrix() {
      const context = document.getElementById("chart-matrix").getContext("2d");
      const ex_matrix = [];

      for (let i = 1; i <= 5; i++) {
        for (let j = 1; j <= 5; j++) {
          ex_matrix.push({
            x: i,
            y: j,
            v: (i - 1) * 5 + j + 10,
          });
        }
      }

      const ex_data = {
        datasets: [
          {
            label: "My Matrix",
            data: ex_matrix,
            backgroundColor(context) {
              const value = context.dataset.data[context.dataIndex].v;
              const alpha = (value - 5) / 40;
              return `rgba(0, 128, 0, ${alpha})`;
            },
            borderColor(context) {
              const value = context.dataset.data[context.dataIndex].v;
              const alpha = (value - 5) / 40;
              return `rgba(0, 100, 0, ${alpha})`;
            },
            borderWidth: 1,
            width: ({ chart }) =>
              ((chart.chartArea || {}).width || 0) /
                Math.sqrt(ex_matrix.length) -
              1,
            height: ({ chart }) =>
              ((chart.chartArea || {}).height || 0) /
                Math.sqrt(ex_matrix.length) -
              1,
          },
        ],
      };

      this.matrix = new Chart(context, {
        type: "matrix",
        data: ex_data,
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
  },
  mounted() {
    this.renderMatrix();
  },
};
</script>

<style>
#chart-matrix {
  max-width: 100%;
  max-height: 100%;
}
</style>
