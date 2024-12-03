<template>
  <Drawer v-model:visible="visible" header="Drawer" position="top" style="width: 30%;">
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod

    </p>
    <Button @click="updateDrawerVisibility">Deactivate Drawer</Button>
  </Drawer>
  <Button @click="updateDrawerVisibility">Activate Drawer</Button>
</template>

<script>
import { ref } from "vue";
import Drawer from "primevue/drawer";
import Button from "primevue/button";

export default {
  setup() {
    const visible = ref(false);
    return {
      visible
    }
  },
  components: {
    Drawer,
    Button,
  },
  methods: {
    updateDrawerVisibility() {
      this.visible = !this.visible;
    }
  }
};
</script>

<style>
@import "../assets/main.css";
</style>
