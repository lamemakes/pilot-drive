<template>
  <div>
    <InfoBar />
    <router-view />
    <div id="nav-container">
      <NavButtons />
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, provide, ref, watch } from "vue";
import NavButtons from "./components/Navigation/NavButtons.vue";
import InfoBar from "./components/InfoBar/InfoBar.vue";
import { BluetoothStore } from "./stores/BluetoothStore";
import { SettingsStore } from "./stores/SettingsStore";
import { UpdateStore } from './stores/UpdateStore';
import { setGlobalTheme } from "./utils/theme";
import { MediaStore } from "./stores/MediaStore";
import { initializeWebSocket } from "./utils/backend";
import { Data } from "./types/Data.interface";
import { VehicleStore } from "./stores/VehicleStore";
import { PhoneStore } from "./stores/PhoneStore";

export default defineComponent({
  components: {
    NavButtons,
    InfoBar
  },
  setup() {
    // Initialize stores
    const bluetoothStore = ref(BluetoothStore);
    const settingsStore = ref(SettingsStore);
    const mediaStore = ref(MediaStore);
    const vehicleStore = ref(VehicleStore)
    const phoneStore = ref(PhoneStore)
    const updateStore = ref(UpdateStore)

    const websocket = initializeWebSocket();
    websocket.onmessage = (message) => {
        const dataObj = JSON.parse(message.data) as Data;
        console.debug(dataObj);
        if (dataObj.hasOwnProperty('type')){

            switch (dataObj.type) {
                case 'bluetooth':
                  if (dataObj.bluetooth){
                    bluetoothStore.value = dataObj.bluetooth;
                  }
                  break;
                  case 'vehicle':
                  if (dataObj.vehicle){
                    vehicleStore.value = dataObj.vehicle;
                  }
                  break;
                case 'media':
                  if (dataObj.media) {
                    mediaStore.value = dataObj.media;
                  }
                  break;
                case 'phone':
                  if (dataObj.phone) {
                    phoneStore.value = dataObj.phone
                  }
                  break;
                case 'updater':
                  if (dataObj.updater) {
                    updateStore.value = dataObj.updater
                  }
                  break;
                case 'settings':
                  if (dataObj.settings) {
                    settingsStore.value = dataObj.settings;
                    setGlobalTheme(settingsStore.value.selectedTheme);
                  }
                  break;
                default:
                  console.error(`Unrecognized websocket type: "${dataObj.type}"`)
            }
        }
    }

    provide('bluetoothStore', bluetoothStore);
    provide('settingsStore', settingsStore);
    provide('mediaStore', mediaStore);
    provide('vehicleStore', vehicleStore);
    provide('phoneStore', phoneStore);
    provide('updateStore', updateStore);
    provide('websocket', ref(websocket));

    onMounted(() => {
      setGlobalTheme(settingsStore.value.selectedTheme);
    })

  }
})
</script>

<style lang="scss">
@font-face{
  font-family: Futura;
  src: local('Futura'), url(assets/fonts/Futura.ttf) format('truetype');
}

* {
  font-family: Futura;
}

#app {
  height: 100%;
  background-color: var(--primary-color);
}

#nav-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  position: absolute;
  bottom: 30px;
  width: 100%;
  z-index: 1;
}
</style>
