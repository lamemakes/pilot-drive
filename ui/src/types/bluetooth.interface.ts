export interface BluetoothDevice {
    hostEnabled: boolean;
    connected: boolean;
    connectedName: string | undefined,
    localHostname?: string | undefined,
    battery?: number | undefined,
    address?: string | undefined
}