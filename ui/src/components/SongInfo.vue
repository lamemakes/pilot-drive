<template>
    <div v-if="mediaStore && mediaStore.song" id="song-info-container">
        <div id="song-info">
            <div id="title">
                <span>{{ formatTitleAlbum(mediaStore.song.title) }}</span>
            </div>
            <div v-if="mediaStore.song.artist" id="artist">
                <span>{{ mediaStore.song.artist }}</span>
            </div>
            <div v-if="mediaStore.song.album" id="album">
                <span>{{ formatTitleAlbum(mediaStore.song.album) }}</span>
            </div>
        </div>
        <div class="progressbar" v-if="mediaStore.song.duration && mediaStore.song.position">
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
import { Media } from '../types/Media.interface';

export default defineComponent({
    components: { SongControl },
    setup () {
        
        const mediaStore = ref((inject("mediaStore") as Media));

        const progress = ref(0);

        const progInterval = 1000

        const progbarUpdate = setInterval( () => {
            if (mediaStore.value.song && mediaStore.value.song.duration && mediaStore.value.song.position){
                const percent = (mediaStore.value.song.position / mediaStore.value.song.duration) * 100
                progress.value = percent > 100 ? 100 : percent // Confirm it doesn't get larger than 100%
                if (mediaStore.value.song.playing) {
                    mediaStore.value.song.position += progInterval;
                }
                console.log(mediaStore.value.song.position)
            }
        }, progInterval)

        const formatTitleAlbum = (titleOrAlbum: string | undefined): string | undefined => {
            // if a track is too long, remove the features in the title using common characteristics of titles
            const MAX_LEN = 40 // Max length of song title, ideally this will be dynamic in the future
            const feature_regex = /((\(|\[|\{)(feat|prod|ft).*(\)|\]|\}))/gi
            if (titleOrAlbum && titleOrAlbum.length > MAX_LEN) {
                return titleOrAlbum.replace(feature_regex, '')
            }
            return titleOrAlbum
        }

        return {mediaStore, progress, formatTitleAlbum}
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

#album, #artist {
    font-size: 32px;
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