<template>
  <Drawer id="drawer" v-model:visible="visible" position="top">
    <Button @click="changeTheme"
      ><img src="../assets/de.png" style="width: 30px; height: 20px"
    /></Button>
    <Button @click="updateDrawerVisibility"
      ><img src="../assets/en.png" style="width: 30px; height: 20px"
    /></Button>
    <Button @click="updateDrawerVisibility"
      ><img src="../assets/de.png" style="width: 30px; height: 20px"
    /></Button>
  </Drawer>
  <Button id="drawer-button" @click="updateDrawerVisibility">
    <span></span>
    <span>-</span>
    <span>-</span>
    <span></span>
  </Button>
</template>

<script>
import { ref } from "vue";
import Drawer from "primevue/drawer";
import Button from "primevue/button";

export default {
  setup() {
    return {};
  },
  data() {
    const body = document.body;
    const visible = ref(false);
    const darkMode = ref(false);
    return {
      visible,
      body,
      darkMode,
    };
  },
  components: {
    Drawer,
    Button,
  },
  methods: {
    updateDrawerVisibility() {
      this.visible = !this.visible;
    },
    changeTheme(){
      if(!this.darkMode){
        this.body.classList.toggle('dark-theme')
        this.darkMode = true;
      }
      if(this.darkMode){
        this.body.classList.toggle('light-theme')
        this.darkMode = false;
      }
    },
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
;