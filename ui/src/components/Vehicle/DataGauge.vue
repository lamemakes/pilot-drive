<template>
    <div v-if="stats" class="gauge-container">
        <div>
            <p class="name">{{ stats.name }}</p>
            <p class="quantity">{{ stats.value.quantity.toFixed(1) }}</p>
            <p class="units">{{ stats.value.unit.replaceAll('_', ' ') }}</p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, toRef } from 'vue'
import { Stats } from '../../types/Vehicle.interface'

export default defineComponent({
    props: {
        stats: Object as PropType<Stats>
    },
    setup (props) {
        const stats = toRef(props, 'stats')

        return {stats}
    }
})
</script>

<style scoped lang="scss">
.gauge-container {
    background-color: var(--secondary-color);
    width: 150px;
    height: 150px;
    display: grid;
    text-align: center;
    border: 5px solid var(--accent-color);
    border-radius: 50%;
    align-items: center;
    margin-top: 20px;
    margin-bottom: 20px;
    p {
        margin: 0px;
    }
}

.quantity {
    font-size: 40px;
}


</style>