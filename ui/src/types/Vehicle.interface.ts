export interface Vehicle {
    enabled: boolean, // Is OBD reading enabled?
    failures: boolean,
    connected: boolean,
    stats: Stats[]
}

export interface Stats {
    name: string,
    value: {
        quantity: number,
        unit: string,
        magnitude: number
    }
}