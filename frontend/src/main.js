import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import PrimeVue from "primevue/config";
import Aura from "@primevue/themes/aura/";
import VueApexCharts from "vue3-apexcharts";
import "./assets/main.css";

const app = createApp(App);

app.use(router);
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      prefix: "p",
      darkModeSelector: ".dark-theme",
      cssLayer: false,
    },
  },
});
app.use(VueApexCharts);

app.mount("#app");
//make vue communicate with Django
//createApp(App).mount("#app");
