export interface Vehicle {
    enabled: boolean, // Is OBD reading enabled?
    connected: boolean,
    speed: number | undefined,
    fuelLevel: number | undefined,
    voltage: number | undefined,
    rpm: number | undefined,
    engineLoad: number | undefined,
    dtc: boolean
}