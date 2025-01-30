// src/utils/nodeUtils.js

import Industry from "@/assets/node_images/consumer/Industry.png";
import City from "@/assets/node_images/consumer/City.png";
import House from "@/assets/node_images/consumer/House.png";

import Battery from "@/assets/node_images/misc/battery.png";
import Junction from "@/assets/node_images/misc/junction.png";

import Gas from "@/assets/node_images/producer/Gas.png";
import Coal from "@/assets/node_images/producer/Coal.png";
import Solar from "@/assets/node_images/producer/Solar.png";
import Wind from "@/assets/node_images/producer/Wind.png";

export function getNodeData(label) {
  switch (label) {
    case "Industry":
      return {
        label: "Industry",
        icon: Industry,
        inputs: [0, 1, 2, 3],
      };

    case "City":
      return {
        label: "City",
        icon: City,
        inputs: [0, 1, 2, 3],
      };

    case "House":
      return {
        label: "House",
        icon: House,
        inputs: [0, 1, 2, 3],
      };

    case "Battery":
      return {
        label: "Battery",
        icon: Battery,
        inputs: [0, 1],
        outputs: [2, 3],
        description: "Stores excess energy and releases it when needed.",
      };

    case "Junction":
      return {
        label: "Junction",
        icon: Junction,
        inputs: [0, 1],
        outputs: [2, 3],
        description: "Connects multiple energy sources and consumers.",
      };

    case "Gas":
      return {
        label: "Gas",
        icon: Gas,
        outputs: [0, 1, 2, 3],
        description:
          "Provides large-scale base power with low carbon emissions.",
      };

    case "Coal":
      return {
        label: "Coal",
        icon: Coal,
        outputs: [0, 1, 2, 3],
        description: "Traditional fossil fuel energy source.",
      };

    case "Solar":
      console.log("test");
      return {
        label: "Solar",
        icon: Solar,
        outputs: [0, 1, 2, 3],
        description: "Generates renewable energy from sunlight.",
      };

    case "Wind":
      return {
        label: "Wind",
        icon: Wind,
        outputs: [0, 1, 2, 3],
        description: "Generates renewable energy from wind.",
      };

    default:
      console.warn(`Unknown node type: ${label}`);
      return null;
  }
}
