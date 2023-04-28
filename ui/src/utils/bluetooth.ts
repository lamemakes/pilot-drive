import { Device } from "../types/Bluetooth.interface";

export function getConnectedDevices(devices: Device[]) {
    const connectedDevices = []
    for (let i =0; i < devices.length; i++) {
        let device = devices[i];
        if (device.connected) connectedDevices.push(device)
    }
    return connectedDevices
}