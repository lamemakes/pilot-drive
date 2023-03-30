import { reactive } from "vue";
import { BluetoothDevice } from "../types/Bluetooth.interface";

export let BluetoothStore: BluetoothDevice = reactive({
    hostEnabled: false,
    connected: false,
    connectedName: undefined,
    localHostname: undefined
})