import { BluetoothDevice } from "./Bluetooth.interface";

export interface Phone {
    enabled: boolean,
    type: 'android' | 'ios' | undefined,
    state: 'connected' | 'locked' | 'disconnected' | 'untrusted',
    notifications: PhoneNotification[]
}

export interface PhoneNotification {
    id: number,
    app_id: string,
    app_name: string,
    title: string,
    time: number,
    body?: string
}

export interface NoNotificationMessage {
    message: string,
    icon: string
}