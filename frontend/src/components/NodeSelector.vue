<template>
    <div class="node-selector">
        <Button @click="handleButtonClick('Button 1')">Button 1</Button>
        <button @click="handleButtonClick('Button 2')">Button 2</button>
        <button @click="handleButtonClick('Button 3')">Button 3</button>
        <select v-model="selectedOption">
            <option disabled value="">Please select one</option>
            <option v-for="option in options" :key="option" :value="option">{{ option }}</option>
        </select>
    </div>
</template>

<script>
export default {
    name: 'NodeSelector',
    data() {
        return { 
            selectedOption: '',
            options: ['Option 1', 'Option 2', 'Option 3']
        };
    },
    methods: {
        handleButtonClick(buttonName) {
            console.log(`${buttonName} clicked`);
        }
    }
};
</script>

<style scoped>
.node-selector {
    display: flex;
    flex-direction: column;
    align-items: center;
}

button {
    margin: 5px;
}

select {
    margin: 10px;
}
</style>