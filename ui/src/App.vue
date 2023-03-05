<template>
  <InfoBar />
  <router-view />
  <div id="nav-container">
    <NavButtons />
  </div>
</template>

<script lang="ts">
import { defineComponent, provide, ref, watch } from "vue";
import NavButtons from "./components/NavButtons.vue";
import InfoBar from "./components/InfoBar.vue";
import { BluetoothStore } from "./stores/BluetoothStore";
import { SettingsStore } from "./stores/SettingsStore";
import { setGlobalTheme } from "./utils/theme";
import { MediaStore } from "./stores/MediaStore";
import { initializeWebSocket } from "./utils/backend";
import { Data } from "./types/data.interface";

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

    const websocket = initializeWebSocket();
    websocket.onmessage = (message) => {
        const dataObj = JSON.parse(message.data) as Data;
        console.error(dataObj);
        if (dataObj.hasOwnProperty('type')){

            switch (dataObj.type) {
                case 'bluetooth':
                  if (dataObj.bluetooth){
                    bluetoothStore.value = dataObj.bluetooth;
                  }
                  break;
                case 'media':
                  if (dataObj.media) {
                    mediaStore.value = dataObj.media;
                  }
                  break;
                case 'phone':
                  if (dataObj.phone) {
                    console.log(dataObj.phone) // TODO: phone implementation
                  }
                  break;
                case 'settings':
                  console.log("SETTINGS!")
                  if (dataObj.settings) {
                    console.log(dataObj.settings.selectedTheme)
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
    provide('websocket', ref(websocket));

  }
})
</script>

<style lang="scss">
@font-face{
  font-family: Futura;
  src: local('Futura'), url(./src/assets/fonts/Futura.ttf) format('truetype');
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
  div {
    margin-inline: 20px;
  }
}
</style>
