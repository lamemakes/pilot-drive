import { reactive } from "vue";
import { Vehicle } from "../types/Vehicle.interface";

export let VehicleStore:Vehicle = reactive({
    enabled: false,
    connected: false,
    failures: false,
    stats: []
})