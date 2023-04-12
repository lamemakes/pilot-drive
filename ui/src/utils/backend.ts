// Utils to handle the websocket/REST calls to the backend
import { inject } from "vue";
import BackendConstants from "../constants/backend";
import { Data } from "../types/Data.interface";

export function initializeWebSocket() {
    const websocket = new WebSocket(BackendConstants.WS_HOST);
    return websocket
}