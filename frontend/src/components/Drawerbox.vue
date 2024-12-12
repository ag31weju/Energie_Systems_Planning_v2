<template>
  <Drawer id="drawer" v-model:visible="visible" position="top">
    <Button @click="changeTheme" class="button"> {{ currentTheme }} </Button>
    <Button @click="changeLanguageEvent('EN')" class="button"
      ><img src="../assets/en.png" style="width: 30px; height: 20px" />
    </Button>
    <Button @click="changeLanguageEvent('DE')" class="button"
      ><img src="../assets/de.png" style="width: 30px; height: 20px"
    /></Button>
  </Drawer>
  <Button id="drawer-button"  @click="visible = !visible">
    <div class="hamburger-menu">
      <div class="line"></div>
      <div class="line"></div>
      <div class="line"></div>
    </div>
  </Button>
</template>

<script>
import { ref } from "vue";
import Drawer from "primevue/drawer";
import Button from "primevue/button";

export default {
  setup(prop, context) {
    const body = document.body;
    const visible = ref(false);
    const darkMode = ref(false);

    const light = "☀️";
    const dark = "🌑";
    const currentTheme = ref(light);

    function changeTheme() {
      if (!darkMode.value) {
        darkMode.value = true;
        currentTheme.value = dark;
      } else {
        darkMode.value = false;
        currentTheme.value = light;
      }
      body.classList.toggle("dark-theme");
    }

    function changeLanguageEvent(language) {
      context.emit('changeLanguage', language);
    }

    return {
      changeTheme,
      changeLanguageEvent,
      visible,
      body,
      darkMode,
      currentTheme,
    };
  },
  components: {
    Drawer,
    Button,
  },
  emits: ['changeLanguage']
};
</script>

<style>
@import "../assets/main.css";
</style>
;
