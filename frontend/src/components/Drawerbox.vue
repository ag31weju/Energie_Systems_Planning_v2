<template>
  <Drawer v-model:visible="visible" header="Drawer" position="top" style="width: 30%;">
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod

    </p>
    <Button @click="visible = false">Deactivate Drawer</Button>
  </Drawer>
  <Button @click="visible = true">Activate Drawer</Button>
</template>

<script>
import { ref } from "vue";
import Drawer from "primevue/drawer";
import Button from "primevue/button";

const visible = ref(false);

export default {
  components: {
    Drawer,
    Button,
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
