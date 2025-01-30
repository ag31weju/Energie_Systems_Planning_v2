import { defineStore } from "pinia";
import { ref } from "vue";

export const useChartsDesignStore = defineStore("useChartsDesignStore", () => {
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

  return { lineChartOptions, barChartOptions };
});
