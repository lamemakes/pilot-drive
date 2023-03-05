<template>
    <div v-for="item in routes" :key="item.name" class="route-btn">
        <router-link :to="{ name: item.name}">
            <img class="route-img" :src="getImageUrl(NAV_ICON_PATH + item.name + '.svg')" />
        </router-link>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, onMounted, ref, watch, watchEffect } from 'vue'
import { routes } from "../constants/routes"
import { Settings } from '../types/settings.interface';
import { ColorVars, handleIconLumin} from '../utils/theme';

export default defineComponent({
    setup () {
        const settingsStore = ref(inject('settingsStore') as Settings);

        const NAV_ICON_PATH = "../assets/icons/";

        const getImageUrl = (name: string) => {
            return new URL(name, import.meta.url).href
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
        

        return {routes, NAV_ICON_PATH, getImageUrl}
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
</style>