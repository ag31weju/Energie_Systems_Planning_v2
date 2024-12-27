<template>
  <div id="drawerbox">
    <Drawerbox @changeLanguage="updateLanguage"></Drawerbox>
  </div>

  <Playfield></Playfield>
</template>

<script>
import { ref } from "vue";
import Playfield from "../components/Playfield.vue";
import Drawerbox from "@/components/Drawerbox.vue";
import ENLang from "@/assets/languages/en.json";
import DELang from "@/assets/languages/de.json";

export default {
  setup() {
    return {};
  },
  components: {
    Playfield,
    Drawerbox,
  },
};
</script>
<style></style>
