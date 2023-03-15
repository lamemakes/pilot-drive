import { reactive } from "vue";
import { Vehicle } from "../types/vehicle.interface";

export let VehicleStore:Vehicle = reactive({
    enabled: false,
    connected: false,
    stats: []
})