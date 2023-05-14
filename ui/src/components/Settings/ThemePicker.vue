<template>
    <div id="picker-container">
        <div v-for="theme in settingsStore.themes" :key="theme.name" id="btn-container" @click="setTheme(theme.name)">
            <div class="accent-circle circle" :style="getBackgroundString(theme.accent)">
                <div class="primary-circle circle" :style="getBackgroundString(theme.primary)">
                    <div class="secondary-circle circle" :style="getBackgroundString(theme.secondary)"></div>
                </div>
            </div>
            <div id="underline" :class="(theme.name === settingsStore.selectedTheme) ? 'active-theme' : ''"></div>
        </div>
    </div>
</template>

<script lang="ts">

import { defineComponent, inject, ref } from 'vue'
import { Settings } from '../../types/Settings.interface';
import { getRgbString } from '../../utils/theme';

export default defineComponent({
    props: {
        setTheme: Function
    },
    setup (props) {
        const settingsStore = ref(inject('settingsStore') as Settings);

        const getBackgroundString = (color: number[]): string => {
            return `background-color: ${getRgbString(color)};`
        }

        const setTheme = (props.setTheme) ? props.setTheme : () => {}

        return {settingsStore, getRgbString, getBackgroundString, setTheme}
    }
})
</script>

<style scoped lang="scss">
#picker-container {
    display: flex;
    flex-direction: row;
}

#btn-container {
    display: grid;
    justify-items: center;
}

.active-theme {
    width: 80%;
    border-bottom: 5px solid var(--accent-color);
}

.circle {
    border-radius: 50%;
    height: 100%;
    width: 100%;
}

.accent-circle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 55px;
    height: 55px;
    margin: 5px;
}

.primary-circle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 45px;
    height: 45px;
}

.secondary-circle {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 20px;
    height: 20px;
}
</style>