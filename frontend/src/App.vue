<template>
  <div id="app">
    <h1>Vue.js Frontend</h1>
    <h1></h1>
    <button @click="fetchMessage">Fetch Message</button>
    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      message: '',
    };
  },
  methods: {
    async fetchMessage() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/');
        this.message = response.data.message;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
  },
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
}
</style>
