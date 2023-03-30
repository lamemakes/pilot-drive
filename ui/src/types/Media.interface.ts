export interface Media {
    source: "bluetooth" | "radio" | "files" | undefined,
    radio: Radio | undefined,
    song: Song | undefined // Files should be of Song type.
}

export interface Song {
    title: string | undefined,
    artist: string | undefined,
    album: string | undefined,
    duration: number | undefined,
    position: number | undefined,
    isPlaying: boolean,
    cover: Blob | undefined
}

export interface Radio {
    stationAddress: number | undefined,
    stationName: string | undefined,
    title: string | undefined,
    artist: string | undefined,
    album: string | undefined,
    cover: Blob | undefined
}