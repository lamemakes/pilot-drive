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
        <div class="option" id="updates">
            <p class="option-title">Updates</p>
            <!-- TODO: this logic statement needs refactoring, wild -->
            <div class="single-btns btns" :class="(updateHasInfo(updateStore) && updateStore.error) ? 'failed-btn' : (updateHasInfo(updateStore) && updateStore.update) ? 'ready-btn' : ''">
                <Updater />
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, Ref, ref } from 'vue'
import ThemePicker from './ThemePicker.vue';
import { Settings } from '../../types/Settings.interface';
import { setGlobalTheme } from '../../utils/theme';
import Updater from './Updater.vue';
import { Updates } from '../../types/Updates.interface';

export default defineComponent({
    components: {ThemePicker, Updater},
    setup () {
        const settingsStore = ref(inject('settingsStore') as Settings);
        const updateStore = ref(inject('updateStore') as Updates);
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

        // TODO: Duplicated code from Updater.vue
        const updateHasInfo = (updateObj: Updates): boolean => {
            return (updateObj.error || updateObj.update) ? true : false
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

        return {settingsStore, updateStore, setTheme, setTfFormat, setMetric, updateHasInfo}
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
    width: 40%;
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
        box-shadow: 0px 2px 2px black;
    }

    .inactive {
        cursor: pointer;
    }
    .active {
        transform:translateY(2px);
        box-shadow: 0 0 0;
    }
}

.single-btns {
    text-align: center;
    display: grid;
    background-color: var(--secondary-color);
    height: 100%;
    padding-top: 6px;
    padding-bottom: 2px;
    box-shadow: 0px 2px 2px black;
    cursor: pointer;
}

.ready-btn {
    background-color: rgb(104, 183, 104);
}

.failed-btn {
    background-color: rgb(188, 81, 81);
    cursor: default;
    box-shadow: none
}

</style>