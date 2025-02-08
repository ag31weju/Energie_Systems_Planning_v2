<template>
  <div class="custom-node" :class="{ highlighted: isHighlighted }" @mouseover="handleMouseOver"
    @mouseleave="handleMouseLeave" @click="handleClick">
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

    const handleClick = () => {
      alert("Node clicked");
    };

    return {
      Position,
      isHighlighted,
      iconSize,
      handleMouseOver,
      handleMouseLeave,
      handleClick,
    };
  },
});
</script>



<style>
.custom-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  /* Smooth animation */
}

.custom-node.highlighted {
  transform: scale(1.2);
  /* Enlarge the node */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  /* Add a shadow for highlighting */
}

.consumer-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.consumer-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.node-name {
  margin-top: 8px;
  /* Adds space between the image and "Hello" */
  font-size: 14px;
  color: #333;
  text-align: center;
}
</style>
