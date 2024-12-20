<template>
  <div>
    <div class="consumer-icon">
      <img :src="data.icon" alt="Consumer Icon" />
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
import { Handle, Position } from "@vue-flow/core";

export default {
  name: "ConsumerNode",
  props: {
    data: {
      type: Object,
      required: true,
    },
  },
  components: {
    Handle
  },
  data() {
    return {
      Position
    };
  }
};
</script>
<style>
.custom-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
 
  color: #fff;
  
 
}

.consumer-icon {
  width: 64px;
  height: 64px;
 
}

</style>
