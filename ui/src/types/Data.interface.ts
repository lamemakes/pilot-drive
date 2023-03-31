// Data types incoming from the backend

import { BluetoothDevice } from "./Bluetooth.interface";
import { Media } from "./Media.interface";
import { Phone } from "./Phone.interface";
import { Settings } from "./Settings.interface";
import { Vehicle } from "./Vehicle.interface";

export interface Data {
    type: "bluetooth" | "media" | "phone" | "vehicle" | 'settings',
    bluetooth?: BluetoothDevice,
    media?: Media,
    phone?: Phone,
    vehicle?: Vehicle,
    settings?: Settings
}