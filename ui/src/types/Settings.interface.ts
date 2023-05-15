export interface Settings {
    version: string,
    tfHourTime: boolean,
    metricUnits: boolean,
    phoneEnabled: boolean,
    vehicleEnabled: boolean,
    selectedTheme: string,
    home: string,
    themes: Theme[]
}

export interface Theme {
    name: string
    primary: number[],
    accent: number[],
    secondary: number[]
}