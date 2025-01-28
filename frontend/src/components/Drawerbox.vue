<template>
  <Drawer id="drawer" v-model:visible="visible" position="top">
    <Button @click="currTheme.toggleTheme" class="button">
      {{ currTheme.themeSymbol }}
    </Button>
    <Button @click="currLang.changeLang('EN')" class="button"
      ><img src="../assets/en.png" style="width: 30px; height: 20px" />
    </Button>
    <Button @click="currLang.changeLang('DE')" class="button"
      ><img src="../assets/de.png" style="width: 30px; height: 20px"
    /></Button>
  </Drawer>
  <Button id="drawer-button" @click="visible = !visible">
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
import { usedLanguage, usedTheme } from "../assets/stores/pageSettings";

export default {
  setup(prop, context) {
    const currLang = usedLanguage();
    const currTheme = usedTheme();
    const visible = ref(false);

    // const body = document.body;

    // const darkMode = ref(false);

    // const light = "☀️";
    // const dark = "🌑";
    // const currentTheme = ref(light);

    // function changeTheme() {
    //   if (!darkMode.value) {
    //     darkMode.value = true;
    //     currentTheme.value = dark;
    //   } else {
    //     darkMode.value = false;
    //     currentTheme.value = light;
    //   }
    //   body.classList.toggle("dark-theme");
    //   context.emit("changeMatrixTheme", darkMode.value);
    // }

    // function changeLanguageEvent(language) {
    //   context.emit("changeLanguage", language);
    // }

    return {
      visible,
      currLang,
      currTheme,
    };
  },
  components: {
    Drawer,
    Button,
  },
  // emits: ["changeLanguage", "changeMatrixTheme"],
};
</script>

<style>
@import "../assets/main.css";
</style>
