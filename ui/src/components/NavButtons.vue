<template>
    <div v-for="item in routes" :key="item.name" class="route-btn">
        <router-link :to="{ name: item.name}" v-if="isEnabled(item)" class="nav-link">
            <img class="route-img" :src="item.icon" />
        </router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, onMounted, Ref, ref, watch, watchEffect } from 'vue'
import { routes, route } from "../constants/routes"
import { Settings } from '../types/Settings.interface';
import { ColorVars, handleIconLumin} from '../utils/theme';

export default defineComponent({
    setup () {
        const settingsStore = ref(inject('settingsStore') as Settings);

        const isEnabled = (route:route) => {
            if (route.conditional === true) {
                const enabledString = `${route.name}Enabled`
                console.error(enabledString)
                const checkEnabled = settingsStore.value[enabledString as keyof Settings] as boolean
                return checkEnabled
            } else {
                return true
            }
        }


        let isDarkLumin = true; // Default value if root can't be queried for whatever reason

        // Handle icon lumin coloring
        onMounted(() => {
            handleIconLumin("route-img", ColorVars.SECONDARY_LUMIN);
        })

        watch(settingsStore, () => {
            handleIconLumin("route-img", ColorVars.SECONDARY_LUMIN);
        },
        {deep: true})
        

        return {routes, isEnabled}
    },
})
</script>

<style scoped lang="scss">
a {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    background-color: var(--secondary-color);
    display: flex;
    justify-content: center;
    align-items: center;
    display: flex;
    justify-content: center;
    align-items: center;
    img {
        width: 70px;
        height: 70px;
    }
}

.router-link-active, router-link-exact-active {
    background-color: var(--accent-color);
}

.nav-link {
    margin-inline: 20px;
}
</style>