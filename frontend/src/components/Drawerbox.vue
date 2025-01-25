<template>
  <Drawer id="drawer" v-model:visible="visible" position="top">
    <Button @click="currTheme.toggleTheme" class="button">
      {{ currTheme.themeSymbol }}
    </Button>
    <Button @click="currLang.changeLang('EN')" class="button"><img src="../assets/en.png"
        style="width: 30px; height: 20px" />
    </Button>
    <Button @click="currLang.changeLang('DE')" class="button"><img src="../assets/de.png"
        style="width: 30px; height: 20px" /></Button>
    <!-- <Select v-model="newColorFilter" :options="currColorBlindnessTheme.colorBlindnessTypes" option-label="label" :placeholder="currColorBlindnessTheme.colorBlindnessTypes[0].label"
      @change="currColorBlindnessTheme.setColorBlindness(newColorFilter)"></Select> -->
      <Select v-model="newColorFilter" :options="currColorBlindnessTheme.colorBlindnessTypes" option-label="label" option-group-label="label" option-group-children="items" :placeholder="currColorBlindnessTheme.colorBlindnessTypes[0].items[0].label"
      @change="currColorBlindnessTheme.setColorBlindness(newColorFilter)"></Select>
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
import { Select, Button, Drawer } from "primevue";
import { usedLanguage, usedTheme, usedColorBlindnessTheme } from "../assets/stores/pageSettings";

export default {
  setup(prop, context) {
    const currLang = usedLanguage();
    const currTheme = usedTheme();
    const currColorBlindnessTheme = usedColorBlindnessTheme();
    const visible = ref(false);
    const newColorFilter = ref(currColorBlindnessTheme);
    return {
      visible,
      currLang,
      currTheme,
      newColorFilter,
      currColorBlindnessTheme,
    };
  },
  components: {
    Drawer,
    Button,
    Select
  },
};
</script>

<style>
@import "../assets/main.css";
</style>
