import { defineStore } from "pinia";
import { ref, shallowRef } from "vue";

export const useChartsDesignStore = defineStore("useChartsDesignStore", () => {
  const barChartOptions = shallowRef({
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
        display: true,
        stacked: true,
      },
      y: {
        display: true,
        stacked: true,
      },
    },
  });

  const lineChartOptions = shallowRef({
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
        display: true,
      },
      y: {
        display: true,
      },
    },
  });

  const colorValues = shallowRef({
    background: [
      "rgba(153, 102, 255, 0.2)",
      "rgba(75, 192, 192, 0.2)",
      "rgba(255, 99, 132, 0.2)",
      "rgba(34, 139, 34, 0.2)",
      "rgba(255, 255, 0, 0.2)",
      "rgba(255, 165, 0, 0.2)",
      "rgba(138, 43, 226, 0.2)",
    ],
    border: [
      "rgba(153, 102, 255, 1)",
      "rgba(75, 192, 192, 1)",
      "rgba(255, 99, 132, 1)",
      "rgba(34, 139, 34, 1)",
      "rgba(204, 204, 0, 1)",
      "rgba(255, 140, 0, 1)",
      "rgba(75, 0, 130, 1)",
    ],
  });

  return { lineChartOptions, barChartOptions, colorValues };
});
