<template>
    <span id="time">
        {{ time }}
    </span>
</template>

<script lang="ts">
import { defineComponent, inject, ref } from 'vue'
import { Settings } from '../types/settings.interface';
import { getTime } from '../utils/date';

export default defineComponent({
    setup () {
        const settingsStore = ref(inject('settingsStore') as Settings);
        
        const time = ref(getTime(settingsStore.value.tfHourTime));

        setInterval(() => time.value = getTime(settingsStore.value.tfHourTime))

        return {time}
    }
})
</script>

<style scoped>

</style>