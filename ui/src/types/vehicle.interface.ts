export interface Vehicle {
    enabled: boolean, // Is OBD reading enabled?
    connected: boolean,
    stats: Stats[]
}

export interface Stats {
    name: string,
    value: {
        quantity: number,
        units: string,
        magnitude: number
    }
}