import { reactive } from "vue";
import { Phone } from "../types/phone.interface";
import { Vehicle } from "../types/vehicle.interface";

export let PhoneStore:Phone = reactive({
    enabled: false,
    type: undefined,
    connected: false,
    state: 'disconnected',
    notifications: []
})