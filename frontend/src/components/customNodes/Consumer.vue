<template>
  <div class="custom-node" :class="{ highlighted: isHighlighted }" @mouseover="handleMouseOver"
    @mouseleave="handleMouseLeave">
    <div class="consumer-icon" :style="{ width: iconSize, height: iconSize }">
      <img :src="data.icon" alt="Consumer Icon" />
    </div>
    <div v-if="isHighlighted" class="node-name" style="color:black; background: rgba(255, 255, 255, 0.7);">
      <!-- color of label -->
      {{ data.label || "Unnamed Node" }}
    </div>
    <div class="handles">
      <!-- Handles for inputs -->
      <div v-for="(input, index) in data.inputs" :key="'input_' + index">
        <Handle type="target" :position="'left'" :id="'input_' + index" style="background: #555" />
        <Handle type="target" :position="'top'" :id="'input_top_' + index" style="background: #555" />
        <Handle type="target" :position="'right'" :id="'input_right_' + index" style="background: #555" />
        <Handle type="target" :position="'bottom'" :id="'input_bottom_' + index" style="background: #555" />
      </div>

      <!-- Handles for outputs -->

    </div>
  </div>
</template>

<script>
import { ref, computed, defineComponent } from "vue";
import { Handle, Position } from "@vue-flow/core";

export default defineComponent({
  name: "ConsumerNode",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  components: {
    Handle,
  },
  setup(props) {
    const isHighlighted = ref(false);

    // Computed property for icon size
    const iconSize = computed(() => {
      return props.data.label === "City" ? "100px" : "50px";
    });

    const handleMouseOver = () => {
      isHighlighted.value = true;
    };

    const handleMouseLeave = () => {
      isHighlighted.value = false;
    };


    return {
      Position,
      isHighlighted,
      iconSize,
      handleMouseOver,
      handleMouseLeave,
    };
  },
});
</script>



<style>
@import "../../assets/main.css";
</style>
