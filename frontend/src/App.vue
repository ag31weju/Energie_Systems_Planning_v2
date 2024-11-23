<template>
  <div id="rootdiv" class="grid-row">
    <div id="outcolumn1" class="grid-column">
      <div id="oc1row" class="grid-row">
        <div id="imagebox" class="grid-column">
          <div id="irr905" class="image-box"></div>
        </div>
        <div id="inputbox" class="grid-column">
          <Slider v-model="sliderVal" style="min-height: 90%; min-width: 90%" class="w-56"/>
        </div>
      </div>
    </div>
    <div id="outercolumn2" class="grid-column">
      <div id="oc2row" class="grid-row">
        <div id="matrix" class="grid-column">
          <label id="i1enmz">Matrix<br /></label>
        </div>
        <div id="charts" class="grid-column">
          <label id="izjjc4">Charts</label>
          <div id="chart1-box" style="background-color: red">
            <p>Hello</p>
            <Chart
              type="bar"
              :data="chartset"
              :options="chartOptions"
              class="h-[30rem]"
            />
          </div>
        </div>
        <div id="checkboxes" class="grid-column">
          <div id="checkboxrow" class="grid-row">
            <div id="cbrow1" class="grid-column">
              <input type="checkbox" id="ibbbfw" />
              <input type="checkbox" id="igod8q" />
              <input type="checkbox" id="ixlfdm" />
            </div>
            <div id="cbrow2" class="grid-column">
              <input type="checkbox" id="ikyips" /><input
                type="checkbox"
                id="i13dy2"
              /><input type="checkbox" id="i00u17" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { ref } from "vue";

const sliderVal = ref(null)

export default {
  data() {
    return {
      message: "",
    };
  },
  methods: {
    async fetchMessage() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/");
        this.message = response.data.message;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    },
  },
};
</script>

<style>
@import "./assets/main.css";
</style>
