<template>
    <div>
        <div class="phone-container" v-if="phoneStore.state == 'connected'">
            <div id="notification-list">
                <div v-for="notification in phoneStore.notifications" :key="notification.id">
                    <PhoneNotification :notification="notification"/>
                </div>
            </div>
        </div>
        <div class="phone-container" id="not-connected" v-else>
            <div id="not-connected-container">
                <div id="not-connected-icon-container">
                    <img class="not-connected-icon" :src="getNotConnectedMessage(phoneStore.state).icon" />
                </div>
                <p>{{ getNotConnectedMessage(phoneStore.state).message }}</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref, watch } from 'vue'
import PhoneNotification from '../components/PhoneNotification.vue';
import { Phone } from '../types/phone.interface';
import { Settings } from '../types/settings.interface';
import { ColorVars, handleIconLumin } from '../utils/theme';


export default defineComponent({
    components: {
        PhoneNotification
    },
    setup () {
        
        const phoneStore = ref(inject('phoneStore') as Phone);
        const settingsStore = ref(inject('settingsStore') as Settings);

        interface NotConnectedDisplay {
            message: string,
            icon: Icons
        }

        enum Icons {
            USB_DISABLED = "../src/assets/icons/usb_disabled.svg",
            PHONE_LOCK = "../src/assets/icons/phone_lock.svg",
            BLUETOOTH_DISABLED = "../src/assets/icons/bluetooth_disabled.svg",
            MOBILE_DISABLED = "../src/assets/icons/mobile_disabled.svg"
        }


        const androidMessageMap = new Map<string, NotConnectedDisplay>([
            ['disconnected', {message: 'Connect an android device via USB and enable USB debugging to see notifications!', icon: Icons.USB_DISABLED}],
            ['locked', {message: 'Unlock your android device to see notifications!', icon: Icons.PHONE_LOCK}],
            ['untrusted', {message: 'Always allow USB debugging from this machine to see notifications!', icon: Icons.PHONE_LOCK}]
        ])

        const iosMessageMap = new Map<string, NotConnectedDisplay>([
            ['disconnected', {message: 'Connect an iOS device via bluetooth to see notifications!', icon: Icons.BLUETOOTH_DISABLED}]
        ])

        const getNotConnectedMessage = (state: string): NotConnectedDisplay => {
            switch(phoneStore.value.type) {
                case 'android': {
                    const androidMessage = androidMessageMap.get(state)
                    if (androidMessage){
                        return androidMessage
                    }
                }
                case 'ios': {
                    const iosMessage = iosMessageMap.get(state)
                    if (iosMessage){
                        return iosMessage
                    }
                }
                default: {
                    console.error(`Invalid phone type "${phoneStore.value.type}"! Returning default not connected.`)
                    return {message: 'Connect a device to see notifications!', icon: Icons.MOBILE_DISABLED}
                }
            }
        }

        watch(settingsStore, () => {
            console.log('ICON HANDLER')
            handleIconLumin('not-connected-icon', ColorVars.SECONDARY_LUMIN);
        },
        {deep: true})

        
        return {phoneStore, getNotConnectedMessage}
    }
})
</script>

<style scoped lang="scss">
.phone-container {
    display: grid;
    justify-items: center;
}

#notification-list {
    display: grid;
    grid-template-columns: auto;
    height: 70vh;
    width: 75%;
    overflow: scroll;
    border-radius: 5vh;
}

#not-connected {
    height: 70vh;
    align-items: center;
}

#not-connected-container {
    color: var(--primary-lumin);
    display: grid;
    justify-items: center;
    p {
        font-size: 25px;
        width: 60%;
        text-align: center;
    }
}

.not-connected-icon {
    height: 15vh;
}
</style>