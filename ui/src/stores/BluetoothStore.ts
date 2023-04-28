import { reactive } from "vue";
import { BluetoothDevice } from "../types/Bluetooth.interface";

export let BluetoothStore: BluetoothDevice = reactive({
        powered: false,
        address: undefined,
        hostname: undefined,
        devices: []
})