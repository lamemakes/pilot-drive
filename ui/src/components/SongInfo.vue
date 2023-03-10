<template>
    <div v-if="songStore && songStore.song" id="song-info-container">
        <div id="song-info">
            <div id="title">
                <span>{{ songStore.song.title }}</span>
            </div>
            <div v-if="songStore.song.artist" id="artist">
                <span>{{ songStore.song.artist }}</span>
            </div>
            <div v-if="songStore.song.album" id="album">
                <span>{{ songStore.song.album }}</span>
            </div>
        </div>
        <div class="progressbar" v-if="songStore.song.duration && songStore.song.position">
            <div class="progressbar" id="progress-inner" :style="{width: progress + '%'}"></div>
        </div>

        <div id="song-ctl">
            <SongControl />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref, watch } from 'vue'
import SongControl from './SongControl.vue';
import { Media } from '../types/media.interface';

export default defineComponent({
    components: { SongControl },
    setup () {
        
        const songStore = ref((inject("mediaStore") as Media));

        const progress = ref(0);

        const progInterval = 1000

        const progbarUpdate = setInterval( () => {
            if (songStore.value.song && songStore.value.song.duration && songStore.value.song.position){
                const percent = (songStore.value.song.position / songStore.value.song.duration) * 100
                progress.value = percent > 100 ? 100 : percent // Confirm it doesn't get larger than 100%
                if (songStore.value.song.isPlaying) {
                    songStore.value.song.position += progInterval;
                }
                console.log(songStore.value.song.position)
            }
        }, progInterval)

        return {songStore, progress}
    }
})
</script>

<style scoped>
#song-info-container{
    width: 100%;
    text-align: center;
    font-size: 40px;
    color: var(--primary-lumin);
}

#title {
    color: var(--accent-color);
}

#song-ctl {
    width: 100%;
    display: grid;
    justify-items: center;
    padding-top: 1%;
}

.progressbar {
    width: 50%;
    height: 8px;
    background-color: var(--secondary-color);
    margin-inline: auto;
    margin-top: 20px;
    margin-bottom: 20px;
    transition: width 500ms;
    border-radius: 8px;
}

#progress-inner {
    background-color: var(--accent-color); 
    margin: 0; 
}


</style>