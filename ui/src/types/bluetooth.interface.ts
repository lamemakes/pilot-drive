export interface BluetoothDevice {
    connected: boolean;
    hostname?: string | undefined,
    battery?: number | undefined,
    macAddress?: string | undefined
}