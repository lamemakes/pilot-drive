import { reactive } from "vue";
import { Phone } from "../types/Phone.interface";
import { Vehicle } from "../types/Vehicle.interface";

export let PhoneStore:Phone = reactive({
    enabled: false,
    type: undefined,
    connected: false,
    state: 'disconnected',
    notifications: []
})