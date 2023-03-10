<template>
    <div id="media-container" v-if="mediaStore.source == 'bluetooth' || mediaStore.source == 'files'">
        <SongInfo />
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref, watch } from 'vue'
import { Media } from '../types/media.interface';
import SongInfo from '../components/SongInfo.vue'

export default defineComponent({
    components: {SongInfo},
    setup () {
        const mediaStore = ref(inject("mediaStore") as Media);
        return {mediaStore}
    }
})
</script>

<style scoped>

#media-container {
    height: 72%;
    display: grid;
    align-items: center;
}

</style>