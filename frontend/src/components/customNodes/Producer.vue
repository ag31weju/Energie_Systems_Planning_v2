<template>
  <div class="custom-node" :class="{ highlighted: isHighlighted }" @mouseover="handleMouseOver"
    @mouseleave="handleMouseLeave" @click="handleClick">
    <div class="producer-icon">
      <img :src="data.icon" alt="Producer Icon" />
    </div>
    <div v-if="isHighlighted" class="node-name">
      {{ data.label || "Unnamed Node" }}
    </div>
    <div class="handles">
      <!-- Handles for inputs -->
      <div v-for="(input, index) in data.inputs" :key="'input_' + index">
        <Handle type="target" :position="Position.Left" :id="input" style="background: #555" />
      </div>

      <!-- Handles for outputs -->
      <div v-for="(output, index) in data.outputs" :key="'output_' + index">
        <Handle type="source" :position="Position.Right" :id="output" style="background: #555" />
      </div>
    </div>
  </div>
</template>



<script>
import { ref, defineComponent } from "vue";
import { Handle, Position } from "@vue-flow/core";

export default defineComponent({
  name: "ProducerNode",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  components: {
    Handle,
  },
  setup() {
    const isHighlighted = ref(false); // Tracks if the node is hovered

    const handleMouseOver = () => {
      isHighlighted.value = true; // Show "Hello" on hover
    };

    const handleMouseLeave = () => {
      isHighlighted.value = false; // Hide "Hello" when hover ends
    };

    const handleClick = () => {
      alert("Node clicked");
    };

    return {
      Position,
      isHighlighted,
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

.producer-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.producer-icon img {
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
