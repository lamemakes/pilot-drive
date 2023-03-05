<template>
    <div v-if="mediaStore.source && ['bluetooth', 'files'].includes(mediaStore.source)">
        <SongInfo />
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref } from 'vue'
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

</style>