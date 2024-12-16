<template>
  <div class="custom-node">
    <img :src="data.icon" alt="Consumer Icon" class="consumer-icon" />
    <span>{{ data.label }}</span>
  </div>
</template>

<script>
export default {
  props: {
    data: Object, // Node data containing 'label' and 'icon'
  },
};
</script>

<style>
.custom-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #ff5733;
  color: #fff;
  border-radius: 0px;
  padding: 0px;
 
}

.consumer-icon {
  width: 64px;
  height: 64px;
  margin-bottom: 5px;
}
</style>
