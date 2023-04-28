import { reactive } from "vue";
import { Media } from "../types/Media.interface";

export let MediaStore:Media = reactive({
    source: 'bluetooth',
    song: {
        title: undefined,
        artist: undefined,
        album: undefined,
        duration: undefined,
        position: undefined,
        playing: false,
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