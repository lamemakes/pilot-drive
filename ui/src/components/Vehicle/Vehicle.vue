<template>
    <div v-if="vehicleStore.connected" class="vehicle-info">
        <DataGauge 
            class="gauge" 
            v-for="stat in stats"
            :key="stat.name"
            :min="getGaugeVals(stat.name).min"
            :max="getGaugeVals(stat.name).max"
            :stats="stat"
            :warn="getGaugeVals(stat.name).warn">
        </DataGauge>
    </div>
    <div v-else id="not-connected">
        <div id="not-connected-container">
            <div id="not-connected-icon-container">
                <img class="not-connected-icon" :src="noCarIcon" />
            </div>
            <p>Not connected to vehicle!</p>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, inject, watch } from 'vue'
import DataGauge from './DataGauge.vue';
import { Settings } from '../../types/Settings.interface';
import { Vehicle } from '../../types/Vehicle.interface';
import { kilometerToMile } from '../../utils/convert';
import noCarIcon from '../../assets/icons/car_issue.svg'

// The type used in the STATS_LUT to hardcode mins/maxes, warn values, and unit converters.
type GaugeVals = {
    min: number,
    max: number,
    warn: number[][],
    imperialConverter?: Function,    // All data comes in as metric, and is then converted based on settings.
    imperialUnit?: string
}

export default defineComponent({
    components: {DataGauge},
    setup () {
        const vehicleStore = ref(inject('vehicleStore') as Vehicle);
        const settingsStore = ref(inject('settingsStore') as Settings)

        // Lookup table for the stats and their mins/maxes/warning ranges
        // warning ranges are expected as an array of number arrays. ie. for a warning range of 0-10 AND 15-18, it would be specified as [[0, 10], [15, 18]]
        const STATS_LUT = {
            speed: {min: 0, max: 130, warn: [[90, 130]], imperialConverter: kilometerToMile, imperialUnit: 'mph'},
            voltage: {min: 0, max: 20, warn: [[0, 11], [15, 20]]},
            rpm: {min: 0, max: 10000, warn: [[7000, 10000]]},
        }

        const getGaugeVals = (name: string): GaugeVals => {
            const gaugeVals = (STATS_LUT as {[index: string]: GaugeVals})[name.toLowerCase()];
            return gaugeVals
        }

        const stats = ref(vehicleStore.value.stats);

        watch(vehicleStore, () => {
            vehicleStore.value.stats.forEach((item, index) => {
                const gaugeVals = getGaugeVals(item.name);
                if (gaugeVals.imperialConverter && gaugeVals.imperialUnit && !settingsStore.value.metricUnits) {
                    stats.value[index].value.quantity = gaugeVals.imperialConverter(item.value.quantity);
                    stats.value[index].value.units = gaugeVals.imperialUnit;
                } else {
                    stats.value[index].value.quantity = item.value.quantity;
                }
            })
        },
        {deep: true})

        return {vehicleStore, stats, getGaugeVals, noCarIcon}
    }
})
</script>

<style scoped lang="scss">
.vehicle-info {
    flex-direction: row;
    display: flex;
    justify-content: center
}

.gauge {
    margin-inline: 1vw;
}

#not-connected {
    display: grid;
    justify-items: center;
}

#not-connected-container, #no-notifs-container {
    color: var(--primary-lumin);
    display: grid;
    justify-items: center;
    p {
        font-size: 25px;
        width: 60%;
        text-align: center;
    }
}

.not-connected-icon, .no-notifs-icon {
    height: 15vh;
}
</style>