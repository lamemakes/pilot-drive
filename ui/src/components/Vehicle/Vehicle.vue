<template>
    <div>
        <div v-if="vehicleStore.connected" class="vehicle-info">
            <DataGauge 
                class="gauge" 
                v-for="stat in stats"
                :key="stat.name"
                :stats="stat">
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
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, inject, watch } from 'vue'
import DataGauge from './DataGauge.vue';
import { Settings } from '../../types/Settings.interface';
import { Vehicle } from '../../types/Vehicle.interface';
import { kilometerToMile, celsiusToFahrenheit, literToGallon, gramToOunce} from '../../utils/convert';
import noCarIcon from '../../assets/icons/car_issue.svg'

// The type used when a value needs to be converted from metric to customary
type ConvertUnit = {
    unit: string,
    converter?: Function
}

export default defineComponent({
    components: {DataGauge},
    setup () {
        const vehicleStore = ref(inject('vehicleStore') as Vehicle);
        const settingsStore = ref(inject('settingsStore') as Settings)

        // Lookup table for metric units to customary
        const unitLookupTable = {
            kilometer_per_hour: {unit: 'miles_per_hour', converter: kilometerToMile},
            kilometer: {unit: 'mile', converter: kilometerToMile},
            degree_celsius: {unit: 'degree_fahrenheit', converter: celsiusToFahrenheit},
            liter_per_hour: {unit: 'gallon_per_hour', converter: literToGallon},
            liter: {unit: 'gallon', converter: literToGallon},
            gram_per_second: {unit: 'ounce_per_second', converter: gramToOunce},
            gram: {unit: 'ounce', converter: gramToOunce}
        } as const;

        const getGaugeConverter = (unitIn: string): ConvertUnit => {
            if (Object.keys(unitLookupTable).includes(unitIn.toLowerCase())) {
                if (!settingsStore.value.metricUnits){
                    const convert = (unitLookupTable as {[index: string]: ConvertUnit})[unitIn.toLowerCase()];
                    return convert
                }
            }

            return {unit: unitIn}
        }

        const stats = ref(vehicleStore.value.stats);

        watch(vehicleStore, () => {
            vehicleStore.value.stats.forEach((item, index) => {
                const converter = getGaugeConverter(item.value.unit)
                if (converter.converter) {
                    stats.value[index].value.quantity = converter.converter(item.value.quantity);
                    stats.value[index].value.unit = converter.unit;
                } else {
                    stats.value[index].value.quantity = item.value.quantity;
                }
            })
        },
        {deep: true})

        return {vehicleStore, stats, noCarIcon}
    }
})
</script>

<style scoped lang="scss">
.vehicle-info {
    flex-direction: row;
    display: grid;
    grid-template-columns: auto auto auto auto;
    justify-content: center;
    height: 70vh;
    overflow: scroll;
}

.gauge {
    margin-inline: 1vw;
    //flex: 0 0 0
}

#not-connected {
    display: grid;
    justify-items: center;
    align-items: center;
    height: 70vh;
}

#not-connected-container {
    color: var(--primary-lumin);
    display: grid;
    justify-items: center;
    p {
        font-size: 25px;
        text-align: center;
    }
}

.not-connected-icon, .no-notifs-icon {
    height: 15vh;
}
</style>