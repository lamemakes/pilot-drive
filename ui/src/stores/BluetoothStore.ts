import { reactive } from "vue";
import { BluetoothDevice } from "../types/bluetooth.interface";

export let BluetoothStore: BluetoothDevice = reactive({
    connected: true,
    hostname: "Pixel 6a"
})