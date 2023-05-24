<template>
    <div id="media-container" v-if="((mediaStore.source === 'bluetooth' && getConnectedDevices(bluetoothStore.devices).length > 0) || mediaStore.source === 'files')">
        <SongInfo />
    </div>
    <div id="no-media-container" v-else>
        <div id="not-connected-container">
            <div id="not-connected-icon-container">
                <img class="not-connected-icon" :src="getNotConnectedMessage()?.icon" />
            </div>
            <div class="not-connected-msg" v-html="getNotConnectedMessage()?.message"></div>
        </div>
        <!-- <div v-if="!bluetoothStore.powered || !getConnectedDevices(bluetoothStore.devices).length">
            <div v-if="!bluetoothStore.powered">
                <TextButton v-if="!bluetoothStore.powered" :text="'Enable Bluetooth'" @click="bluetoothCommand(BluetoothActions.POWER_ON)"/>
                <TextButton v-else :text="'Disable Bluetooth'" @click="bluetoothCommand(BluetoothActions.POWER_OFF)"/>
            </div>
            <div v-else>
                <TextButton v-if="!bluetoothStore.discoverable" :text="'Make Discoverable'" @click="bluetoothCommand(BluetoothActions.START_DISCOVERY)"/>
                <TextButton v-else :text="'Stop Discoverable'" @click="bluetoothCommand(BluetoothActions.STOP_DISCOVERY)"/> 
            </div>
        </div> -->
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref } from 'vue'
import { Media } from '../../types/Media.interface';
import SongInfo from './Song/SongInfo.vue'
import TextButton from '../Button/TextButton.vue';
import { BluetoothDevice } from '../../types/Bluetooth.interface';
import { getConnectedDevices } from '../../utils/bluetooth'
import { NotConnectedDisplay } from '../../types/NotConnectedDisplay.interface';
import bluetoothDisabled from '../../assets/icons/bluetooth_disabled.svg'

export default defineComponent({
    components: {SongInfo, TextButton},
    setup () {
        const mediaStore = ref(inject("mediaStore") as Media);
        const bluetoothStore = ref(inject('bluetoothStore') as BluetoothDevice)
        const websocket = ref(inject('websocket') as WebSocket)

        enum BluetoothActions {
            POWER_ON = 'on-power',
            POWER_OFF = 'off-power',
            START_DISCOVERY = 'start-discovery',
            STOP_DISCOVERY = 'stop-discovery'
        }

        // TODO: Make these string keys Enums
        const noMediaMessageMap = new Map<string, NotConnectedDisplay>([
            ['bluetooth-disabled', {message: '<p>Enable & connect bluetooth to start playing audio!</p>', icon: bluetoothDisabled}],
            ['bluetooth-disconnected', {message: (bluetoothStore.value.hostname) ? `<p>To connect, look for <span id=hostname>${bluetoothStore.value.hostname}</span> in your bluetooth settings</p>` : '<p>Connect a bluetooth device to start playing audio!</p>', icon: bluetoothDisabled}],
        ])

        const getNotConnectedMessage = () => {
            if (mediaStore.value.source == 'bluetooth') {
                if (!bluetoothStore.value.powered){
                    return noMediaMessageMap.get('bluetooth-disabled')
                }
                if (!(getConnectedDevices(bluetoothStore.value.devices).length > 0)) {
                    console.log(bluetoothStore.value.hostname)
                    return noMediaMessageMap.get('bluetooth-disconnected')
                }
            }
        }

        const bluetoothCommand = (command: BluetoothActions) => {
            websocket.value.send(
                JSON.stringify(
                    {
                        type: 'bluetooth',
                        bluetooth: command
                    }
                )
            )
        }

        return {mediaStore, bluetoothStore, getConnectedDevices, getNotConnectedMessage, BluetoothActions, bluetoothCommand}
    }
})
</script>

<style scoped lang="scss">

#media-container {
    display: grid;
    align-items: center;
    height: 70vh;
}

#no-media-container {
    display: grid;
    justify-items: center;
    align-items: center;
    height: 70vh;
}


#not-connected-container {
    color: var(--primary-lumin);
    display: grid;
    justify-items: center;
}

.not-connected-icon {
    height: 15vh;
}

:deep(.not-connected-msg > p) {
    font-size: 25px;
    text-align: center; 
}

:deep(#hostname) {
    color: var(--accent-color);
}

</style>