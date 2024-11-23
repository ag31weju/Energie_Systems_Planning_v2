<template>
  <div id="rootdiv" class="grid-row">
    <div id="outcolumn1" class="grid-column">
      <div id="oc1row" class="grid-row">
        <div id="imagebox" class="grid-column">
          <div id="irr905" class="image-box"></div>
        </div>
        <div id="inputbox" class="grid-column">
          <input type="text" id="inyw9q" />
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
          <div>
            <h1>Chart 1</h1>
            <svg>
              <rect width="100%" height="100" />
            </svg>
          </div>
          <div>
            <h1>Chart 2</h1>
            <svg>
              <rect width="100%" height="100" />
            </svg>
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
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  background-color: rgb(51, 51, 51);
  color: white;
}

.grid-column {
  flex: 1 1 0%;
  padding: 5px 0;
}

.grid-row {
  display: flex;
  justify-content: flex-start;
  align-items: stretch;
  flex-direction: row;
  min-height: auto;
  padding: 10px 0;
}

.grid-column.feature-item {
  padding-top: 15px;
  padding-right: 15px;
  padding-bottom: 15px;
  padding-left: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-width: 30%;
}

.grid-column.testimonial-item {
  padding-top: 15px;
  padding-right: 15px;
  padding-bottom: 15px;
  padding-left: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  min-width: 45%;
  background-color: rgba(247, 247, 247, 0.23);
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  border-bottom-right-radius: 5px;
  border-bottom-left-radius: 5px;
  align-items: flex-start;
  border-top-width: 1px;
  border-right-width: 1px;
  border-bottom-width: 1px;
  border-left-width: 1px;
  border-top-style: solid;
  border-right-style: solid;
  border-bottom-style: solid;
  border-left-style: solid;
  border-top-color: rgba(0, 0, 0, 0.06);
  border-right-color: rgba(0, 0, 0, 0.06);
  border-bottom-color: rgba(0, 0, 0, 0.06);
  border-left-color: rgba(0, 0, 0, 0.06);
}

#rootdiv {
  align-items: stretch;
  height: 100vh;
  padding-top: 0px;
  padding-bottom: 0px;
}

#outercolumn2 {
  padding-top: 0px;
  padding-bottom: 0px;
}

#outcolumn1 {
  display: flex;
  flex-direction: column;
  padding-top: 0px;
  padding-bottom: 0px;
}

#oc1row {
  flex-direction: column;
  height: 100%;
  padding-top: 0px;
  padding-bottom: 0px;
}

#imagebox {
  min-height: 70%;
  display: flex;
  flex-direction: column;
  padding-top: 0px;
  padding-bottom: 0px;
}

#inputbox {
  min-height: 30%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 0px;
  padding-bottom: 0px;
}

.image-box {
  height: 200px;
  width: 100%;
}

#irr905 {
  background-image: url("https://images.pexels.com/photos/2121640/pexels-photo-2121640.jpeg?auto=compress&cs=tinysrgb&w=500&dpr=2");
  background-size: contain;
  background-position: center center;
  background-attachment: scroll;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: row;
  height: 100%;
  width: 100%;
}

#inyw9q {
  display: flex;
  align-items: flex-start;
  flex-direction: row;
  justify-content: flex-start;
  flex-wrap: nowrap;
}

#oc2row {
  flex-direction: column;
  height: 100%;
  padding-top: 0px;
  padding-bottom: 0px;
}

#matrix {
  padding-top: 0px;
  padding-bottom: 0px;
  display: flex;
  flex-direction: column;
}

#charts {
  padding-top: 0px;
  padding-bottom: 0px;
  display: flex;
  flex-direction: column;
  padding-right: 0px;
  padding-left: 0px;
}

#checkboxes {
  padding-top: 0px;
  padding-bottom: 0px;
  display: flex;
  flex-direction: row;
  justify-content: space-evenly;
}

#ibbbfw {
  display: block;
}

#checkboxrow {
  flex-direction: column;
  justify-content: flex-start;
  align-items: stretch;
  padding-top: 0px;
  padding-bottom: 0px;
  min-width: 100%;
}

#cbrow1 {
  display: flex;

  padding-top: 0px;
  padding-bottom: 0px;
  justify-content: space-evenly;
}

#cbrow2 {
  display: flex;
  padding-top: 0px;
  padding-bottom: 0px;
  justify-content: space-evenly;
}

@media (max-width: 992px) {
  .grid-row {
    flex-direction: column;
  }
}
</style>
