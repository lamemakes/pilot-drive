import { BluetoothDevice } from "./bluetooth.interface";

export interface Phone extends BluetoothDevice {
    enabled: boolean,
    connected: boolean,
    deviceType: 'ios' | 'android' | undefined,
    notifications: PhoneNotification[]
}

export interface PhoneNotification {
    subtext: string | undefined,
    title: string | undefined,
    icon: Blob | undefined,
    key: string | undefined,
    packageName: string | undefined,
    priority: string | undefined,
    tickerText: string | undefined,
    time: string | undefined,
}