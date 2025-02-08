<template>
  <div class="custom-node" :class="{
    highlighted: isHighlighted,
    selectedFirst: isSelectedFirst,
    selectedSecond: isSelectedSecond,
  }" @mouseover="handleMouseOver" @mouseleave="handleMouseLeave" @click="handleClick">
    <div class="battery-icon">
      <img :src="data.icon" alt="Battery Icon" />
    </div>
    <div v-if="isHighlighted" class="node-name" style="color:black; background: rgba(255, 255, 255, 0.7);"  > <!-- color of label -->
      {{ data.label || "Battery" }}
    </div>
    <div class="handles">
      <!-- Handles for inputs -->
      <div v-for="(input, index) in data.inputs" :key="'input_' + index">
        <Handle type="target" :position="'left'" :id="'input_' + index" style="background: #555" />
        <Handle type="target" :position="'top'" :id="'input_top_' + index" style="background: #555" />
      </div>

      <!-- Handles for outputs -->
      <div v-for="(output, index) in data.outputs" :key="'output_' + index">
        <Handle type="source" :position="'right'" :id="'output_' + index" style="background: #555" />
        <Handle type="source" :position="'bottom'" :id="'output_bottom_' + index" style="background: #555" />
      </div>
      />
    </div>
  </div>

</template>

<script>
import { ref, inject, defineComponent, computed } from "vue";
import { Handle, Position } from "@vue-flow/core";

export default defineComponent({
  name: "BatteryNode",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  components: {
    Handle,
  },
  setup(props, context) {
    const handleNodeSelection = inject("handleNodeSelection");
    let selectedNodes = inject("selectedNodes")
      ? inject("selectedNodes")
      : undefined;
    const isHighlighted = ref(false); // Tracks if the node is hovered
    const nodeID = context.attrs.id.at(-1);
    const isSelectedFirst = computed(() => {
      return selectedNodes ? selectedNodes.value[0] === nodeID : false;
    });
    const isSelectedSecond = computed(() => {
      return selectedNodes ? selectedNodes.value[1] === nodeID : false;
    });

    const handleMouseOver = () => {
      isHighlighted.value = true; // Show "Hello" on hover
    };

    const handleMouseLeave = () => {
      isHighlighted.value = false; // Hide "Hello" when hover ends
    };

    const handleClick = () => {
      handleNodeSelection(nodeID);
    };

    return {
      Position,
      isHighlighted,
      isSelectedFirst,
      isSelectedSecond,
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
}

.custom-node.highlighted {
  transform: scale(1.2);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.custom-node.selectedFirst {
  box-shadow: 0 0 15px 5px rgba(255, 0, 0, 0.8);
  border: 2px solid black;
  transform: scale(1.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.custom-node.selectedSecond {
  box-shadow: 0 0 15px 5px rgba(0, 0, 255, 0.8);
  border: 2px solid black;
  transform: scale(1.1);
  transition: box-shadow 0.3s ease, transform 0.3s ease;
}

.battery-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.battery-icon img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.node-name {
  margin-top: 8px;
  font-size: 14px;
  color: #333;
  text-align: center;
}
</style>
