<template>
    <div v-if="songStore && songStore.song" class="song-ctrl-btn" id="control-container">
        <div class="song-ctl-btn" id="skip-prev-btn" @click="skipTrack(Skip.prev)">
            <img class="control-icon" :src="Icons.SKIP_PREV_ICON">
        </div>
        <div class="song-ctl-btn" id="status-btn" @click="changeState">
            <img class="control-icon" :src="(songStore.song.isPlaying) ? Icons.PAUSE_ICON : Icons.PLAY_ICON">
        </div>
        <div class="song-ctl-btn" id="skip-next-btn" @click="skipTrack(Skip.next);">
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
        enum Skip {
            prev = -1,
            next = 1
        }

        enum Icons {
            PLAY_ICON = "../src/assets/icons/play.svg",
            PAUSE_ICON = "../src/assets/icons/pause.svg",
            SKIP_PREV_ICON = "../src/assets/icons/skip_prev.svg",
            SKIP_NEXT_ICON = "../src/assets/icons/skip_next.svg"
        }

        const songStore = ref(inject("mediaStore") as Media);
        const settingsStore = ref(inject('settingsStore') as Settings);

        const changeState = () => {
            if (songStore.value.song) {
                songStore.value.song.isPlaying = !songStore.value.song.isPlaying;
                // TODO: Add endpoint call
            }
        }

        const skipTrack = (skip: number) => {
            switch (skip){
                // TODO: Add endpoint call
                case Skip.prev:
                    console.log("Previous Track");
                    break;
                case Skip.next:
                    console.log("Next Track");
                    break
                default:
                    return
            }
        }

        // Handle icon lumin coloring
        onMounted(() => handleIconLumin("control-icon", ColorVars.SECONDARY_LUMIN))

        watch(settingsStore, () => {
            handleIconLumin("route-img", ColorVars.SECONDARY_LUMIN);
        },
        {deep: true})


        return {Icons, songStore, changeState, Skip, skipTrack}
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