<template>
    <div id="settings-container">
        <div class="option" id="theme">
            <p class="option-title">Themes</p>
            <ThemePicker :setTheme="setTheme"/>
        </div>
        <div class="option" id="tf-time">
            <p class="option-title">Time Format</p>
            <div class="bool-btns btns">
                <div class="bool-btn" :class="(settingsStore.tfHourTime) ? 'active' : 'inactive'" @click="setTfFormat(true)">24-Hour</div>
                <div class="bool-btn" :class="(!settingsStore.tfHourTime) ? 'active' : 'inactive'" @click="setTfFormat(false)">12-Hour</div>
            </div>
        </div>
        <div class="option" id="units">
            <p class="option-title">Units</p>
            <div class="bool-btns btns">
                <div class="bool-btn" :class="(settingsStore.metricUnits) ? 'active' : 'inactive'" @click="setMetric(true)">Metric</div>
                <div class="bool-btn" :class="(!settingsStore.metricUnits) ? 'active' : 'inactive'" @click="setMetric(false)">Imperial</div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref } from 'vue'
import ThemePicker from '../components/ThemePicker.vue';
import { Settings } from '../types/Settings.interface';
import { setGlobalTheme } from '../utils/theme';

export default defineComponent({
    components: {ThemePicker},
    setup () {
        const settingsStore = ref(inject('settingsStore') as Settings);
        const websocket = ref(inject('websocket') as WebSocket);

        const pushSettings = () => {
            websocket.value.send(
                JSON.stringify(
                    {
                        type: "settings",
                        settings: settingsStore.value
                    }
                )
            )
        }

        // TODO: More efficient way of doing this
        const setTheme = (selectedTheme: string) => {
            if (selectedTheme === settingsStore.value.selectedTheme) return;
            settingsStore.value.selectedTheme = selectedTheme;
            setGlobalTheme(settingsStore.value.selectedTheme);
            // pushSettingsDebounce();
            pushSettings()
        }

        const setTfFormat = (useTfFormat: boolean) => {
            if (useTfFormat === settingsStore.value.tfHourTime) return;
            settingsStore.value.tfHourTime = useTfFormat;
            // pushSettingsDebounce();
            pushSettings()
        }

        const setMetric = (useMetric: boolean) => {
            if (useMetric === settingsStore.value.metricUnits) return;
            settingsStore.value.metricUnits = useMetric;
            //pushSettingsDebounce();
            pushSettings()
        }

        return {settingsStore, setTheme, setTfFormat, setMetric}
    }
})
</script>

<style scoped lang="scss">
#settings-container {
    display: grid;
    grid-template-rows: auto;
    justify-items: center;
    color: var(--primary-lumin);
    p {
        margin-bottom: 10px;
    }
}

.option {
    display: grid;
    width: 100%;
    grid-template-rows: auto;
    justify-items: center;
}

.btns {
    width: 40%
}

.bool-btns {
    text-align: center;
    display: grid;
    grid-template-columns: 50% 50%;
    grid-gap: 5px;
    justify-items: center;
    .bool-btn {
        background-color: var(--secondary-color);
        width: 100%;
        height: 100%;
        padding-top: 6px;
        padding-bottom: 2px;
    }
    .active {
        mix-blend-mode:hard-light;
    }
}
</style>