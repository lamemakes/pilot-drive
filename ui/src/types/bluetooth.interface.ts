export interface BluetoothDevice {
    connected: boolean;
    connectedName: string | undefined,
    localHostname?: string | undefined,
    battery?: number | undefined,
    address?: string | undefined
}