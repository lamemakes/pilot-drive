import { reactive } from "vue";
import { Media } from "../types/media.interface";

export let MediaStore:Media = reactive({
    source: 'bluetooth',
    song: {
        title: 'Sweatpants',
        artist: 'Childish Gambino',
        album: 'Because the Internet',
        duration: undefined,
        position: undefined,
        isPlaying: false,
        cover: undefined,
    },
    radio: {
        stationAddress: undefined,
        stationName: undefined,
        title: undefined,
        artist: undefined,
        album: undefined,
        cover: undefined
    }
})