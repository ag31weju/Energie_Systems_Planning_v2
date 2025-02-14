import { defineStore } from "pinia";

export const useScenarioStore = defineStore("scenario", {
  state: () => ({
    nodes: [],
    edges: [],
    sliderData: {},
  }),

  actions: {

    saveScenario(nodes, edges) {
      this.nodes = nodes;
      this.edges = edges;
      console.log("Nodes and edges saved in store!");
    },

 
    

    loadScenario() {
      return {
        nodes: this.nodes,
        edges: this.edges,
        sliderData: this.sliderData,
      };
    },
  },
});

