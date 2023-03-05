// Data types incoming from the backend

import { BluetoothDevice } from "./bluetooth.interface";
import { Media } from "./media.interface";
import { Phone } from "./phone.interface";
import { Settings } from "./settings.interface";
import { Vehicle } from "./vehicle.interface";

export interface Data {
    type: "bluetooth" | "media" | "phone" | "vehicle" | 'settings',
    bluetooth?: BluetoothDevice,
    media?: Media,
    phone?: Phone,
    vehicle?: Vehicle,
    settings?: Settings
}