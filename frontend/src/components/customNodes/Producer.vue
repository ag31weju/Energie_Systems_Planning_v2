<template>
  <div
    class="custom-node"
    :class="{
      highlighted: isHighlighted,
      selectedFirst: isSelectedFirst,
      selectedSecond: isSelectedSecond,
    }"
    @mouseover="handleMouseOver"
    @mouseleave="handleMouseLeave"
    @click="handleClick"
  >
    <div class="producer-icon">
      <img :src="data.icon" alt="Producer Icon" />
    </div>
    <div
      v-if="isHighlighted"
      class="node-name"
      style="color: crimson; background: black"
    >
      <!-- color of label -->
      {{ data.label || "Unnamed Node" }}
    </div>
    <div class="handles">
      <!-- Handles for inputs -->
      <div v-for="(input, index) in data.inputs" :key="'input_' + index">
        <Handle
          type="target"
          :position="Position.Left"
          :id="input"
          style="background: #555"
        />
      </div>

      <!-- Handles for outputs -->
      <div v-for="(output, index) in data.outputs" :key="'output_' + index">
        <Handle
          type="source"
          :position="Position.Right"
          :id="output"
          style="background: #555"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, inject, defineComponent, computed } from "vue";
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
  setup(props, context) {
    let handleNodeSelection = inject("handleNodeSelection");
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
      //console.log(context.attrs.id.at(-1)); //id is "node_x" and x is extracted afterwards
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
@import "../../assets/main.css";
</style>