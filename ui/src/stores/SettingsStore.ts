import { Settings } from "../types/settings.interface";
import { Theme } from "../types/settings.interface";
import { reactive } from "vue";

export let SettingsStore: Settings = reactive({
    version: "0.0.0",
    tfHourTime: false,
    metricUnits: false,
    vehicleEnabled: false,
    phoneEnabled: false,
    selectedTheme: "",
    themes: [
        {
            name: "sherbet",
            accent: [ 182, 215, 168 ],
            primary: [ 234, 153, 153 ], 
            secondary: [ 249, 203, 156 ] 
        },
        {
            name: "dark",
            accent: [ 131, 52, 45 ],
            primary: [ 28, 30, 33 ],
            secondary: [ 215, 208, 200 ]
        },
        {
            name: "light",
            accent: [ 221, 113, 98 ],
            primary: [ 236, 241, 250 ],
            secondary: [ 112, 121, 137 ]
        }
    ] as Theme[]
})

//[ 32, 16, 104 ]
//[ 182, 215, 168 ]