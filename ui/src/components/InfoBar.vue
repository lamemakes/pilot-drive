<template>
    <div id="top-row">
        <div id="connected-device">
            <span v-if="bluetoothStore.connected && bluetoothStore.connectedName">
                {{ bluetoothStore.connectedName }}
            </span>
        </div>
        <div id="clock">
            <LiveClock />
        </div>
        <div id="placeholder-div"></div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref } from 'vue'
import { BluetoothDevice } from '../types/bluetooth.interface';
import LiveClock from './LiveClock.vue';

export default defineComponent({
    components: {LiveClock},
    setup () {
        const bluetoothStore = ref(inject("bluetoothStore") as BluetoothDevice);

        return {bluetoothStore}
    }
})
</script>

<style scoped lang="scss">
#top-row {
    display: grid;
    color: var(--primary-lumin);
    grid-template-columns: 33% 33% 33%;
    font-size: 25px;
    padding-bottom: 5px;
    margin-inline: 6px;
}

#connected-device {
    text-align: left;
}

#clock { 
    text-align: center;
}

</style>