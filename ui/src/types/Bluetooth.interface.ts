export interface BluetoothDevice {
    powered: boolean;
    address: string | undefined;
    hostname: string | undefined;
    devices: Device[];
}

export interface Device {
    name: string;
    address: string;
    connected: boolean;
    isMediaSource: boolean;
}