<template>
    <div v-if="songStore && songStore.song" class="song-ctrl-btn" id="control-container">
        <div class="song-ctl-btn" id="skip-prev-btn" @click="skipTrack(TrackActions.PREV)">
            <img class="control-icon" :src="iconMap.get(TrackActions.PREV)">
        </div>
        <div class="song-ctl-btn" id="status-btn" @click="changeState">
            <img class="control-icon" :src="(songStore.song.playing) ? iconMap.get(TrackActions.PAUSE) : iconMap.get(TrackActions.PLAY)">
        </div>
        <div class="song-ctl-btn" id="skip-next-btn" @click="skipTrack(TrackActions.NEXT);">
            <img class="control-icon" :src="iconMap.get(TrackActions.NEXT)">
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, onMounted, ref, watch } from 'vue'
import { Media } from '../../../types/Media.interface';
import { Settings } from '../../../types/Settings.interface';
import { ColorVars, handleIconLumin } from '../../../utils/theme';
import playIcon from '../../../assets/icons/pause.svg'
import pauseIcon from '../../../assets/icons/pause.svg'
import skipPrevIcon from '../../../assets/icons/skip_prev.svg'
import skipNextIcon from '../../../assets/icons/skip_next.svg'

export default defineComponent({
    setup () {

        enum TrackActions {
            PLAY = 'play',
            PAUSE = 'pause',
            NEXT = 'next',
            PREV = 'prev'
        }

        const iconMap = new Map<TrackActions, string>([
            [TrackActions.PLAY, playIcon],
            [TrackActions.PAUSE, pauseIcon],
            [TrackActions.PREV, skipPrevIcon],
            [TrackActions.NEXT, skipNextIcon]
        ])

        const songStore = ref(inject("mediaStore") as Media);
        const settingsStore = ref(inject('settingsStore') as Settings);
        const websocket = ref(inject('websocket') as WebSocket);

        const pushControl = (action: string) => {
            if (songStore.value.source){
                websocket.value.send(
                    JSON.stringify(
                        {
                            type: 'media',
                            'media': action
                        }
                    )
                )
            }
        }

        const changeState = () => {
            if (songStore.value.song) {
                songStore.value.song.playing = !songStore.value.song.playing;
                pushControl(songStore.value.song.playing ? TrackActions.PLAY : TrackActions.PAUSE)
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


        return {iconMap, songStore, changeState, TrackActions, skipTrack}
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