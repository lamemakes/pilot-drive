import { reactive } from "vue";
import { BluetoothDevice } from "../types/Bluetooth.interface";

export let BluetoothStore: BluetoothDevice = reactive({
    enabled: false,
    connected: false,
    connectedName: undefined,
    localHostname: undefined,
    battery: undefined,
    address: undefined
})