import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import PrimeVue from 'primevue/config'

const app = createApp(App);

app.use(router);
app.use(PrimeVue)

app.mount("#app");
//make vue communicate with Django
createApp(App).mount("#app");
