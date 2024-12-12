<template>
  <Panel id="matrix-container" :header="null">
    <table>
      <thead>
        <tr>
          <th></th>
          <th v-for="(_, colIndex) in matrixData[0]" :key="colIndex">
            {{ colIndex }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in matrixData" :key="rowIndex">
          <th>{{ rowIndex }}</th>
          <td
            v-for="(value, colIndex) in matrixData[rowIndex]"
            :key="rowIndex + colIndex"
          >
            {{ value }}
          </td>
        </tr>
      </tbody>
    </table>
  </Panel>
</template>

<script>
import { Panel } from "primevue";

export default {
  props: {
    matrixData: {
      type: Array,
      required: false,
      default: () =>
        Array.from({ length: 6 }, (_, colIndex) => {
          const col = {};
          Array.from({ length: 6 }, (_, rowIndex) => {
            col[rowIndex] = "";
          });
          return col;
        }),
    },
  },
  data() {
    return {};
  },
  components: {
    Panel,
  },
};
</script>

<style scoped>
table {
  border-collapse: collapse;
  width: 100%;
  height: 100%;
}

th,
td {
  border: 1px solid black;
  padding: 10px;
  text-align: center;
  color: var(--matrix-text-color);
}

th {
  background-color: var(--matrix-background-color-header);
}

td {
  background-color: var(--matrix-background-color-cell);
}
</style>
