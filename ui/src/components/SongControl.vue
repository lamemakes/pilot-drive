<template>
    <div v-if="songStore && songStore.song" class="song-ctrl-btn" id="control-container">
        <div class="song-ctl-btn" id="skip-prev-btn" @click="skipTrack(TrackActions.PREV)">
            <img class="control-icon" :src="Icons.SKIP_PREV_ICON">
        </div>
        <div class="song-ctl-btn" id="status-btn" @click="changeState">
            <img class="control-icon" :src="(songStore.song.isPlaying) ? Icons.PAUSE_ICON : Icons.PLAY_ICON">
        </div>
        <div class="song-ctl-btn" id="skip-next-btn" @click="skipTrack(TrackActions.NEXT);">
            <img class="control-icon" :src="Icons.SKIP_NEXT_ICON">
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, onMounted, ref, watch } from 'vue'
import { Media } from '../types/media.interface';
import { Settings } from '../types/settings.interface';
import { ColorVars, handleIconLumin } from '../utils/theme';

export default defineComponent({
    setup () {
        enum Icons {
            PLAY_ICON = "../src/assets/icons/play.svg",
            PAUSE_ICON = "../src/assets/icons/pause.svg",
            SKIP_PREV_ICON = "../src/assets/icons/skip_prev.svg",
            SKIP_NEXT_ICON = "../src/assets/icons/skip_next.svg"
        }

        enum TrackActions {
            PLAY = 'play',
            PAUSE = 'pause',
            NEXT = 'next',
            PREV = 'prev'
        }

        const songStore = ref(inject("mediaStore") as Media);
        const settingsStore = ref(inject('settingsStore') as Settings);
        const websocket = ref(inject('websocket') as WebSocket);

        const pushControl = (action: string) => {
            if (songStore.value.source){
                websocket.value.send(
                    JSON.stringify(
                        {
                            type: songStore.value.source,
                            [songStore.value.source.toString()]: action
                        }
                    )
                )
            }
        }

        const changeState = () => {
            if (songStore.value.song) {
                songStore.value.song.isPlaying = !songStore.value.song.isPlaying;
                pushControl(songStore.value.song.isPlaying ? TrackActions.PLAY : TrackActions.PAUSE)
            }
        }

        const skipTrack = (action: TrackActions) => {
            if (action === TrackActions.NEXT || action === TrackActions.PREV) {
                pushControl(action)
            }
        }

        // Handle icon lumin coloring
        onMounted(() => handleIconLumin("control-icon", ColorVars.SECONDARY_LUMIN))

        watch(settingsStore, () => {
            handleIconLumin("route-img", ColorVars.SECONDARY_LUMIN);
        },
        {deep: true})


        return {Icons, songStore, changeState, TrackActions, skipTrack}
    }
})
</script>

<style scoped lang="scss">
#control-container {
    display: grid;
    grid-template-columns: 33% 33% 33%;
    justify-content: center;
    width: fit-content;
}

.song-ctl-btn {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    background-color: var(--secondary-color);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-inline: 3vw;
    img {
        width: 40px;
        height: 40px; 
    }
}
</style>