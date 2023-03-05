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
        <div id="song-ctl">
            <SongControl />
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref } from 'vue'
import SongControl from './SongControl.vue';
import { Media } from '../types/media.interface';

export default defineComponent({
    components: { SongControl },
    setup () {
        
        const songStore = ref((inject("mediaStore") as Media));

        console.log(songStore.value)

        return {songStore}
    }
})
</script>

<style scoped>
#song-info-container{
    width: 100%;
    text-align: center;
    font-size: 40px;
    padding-top: 12%;
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
</style>