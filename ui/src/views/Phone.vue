<template>
    <div>
        <div class="phone-container" v-if="phoneStore.state == 'connected' && phoneStore.notifications.length > 0">
            <div id="notification-list">
                <div v-for="notification in phoneStore.notifications" :key="notification.id">
                    <PhoneNotification :notification="notification"/>
                </div>
            </div>
        </div>
        <div class="phone-container" id="no-show" v-else>
            <div v-if="phoneStore.state != 'connected'" id="not-connected-container">
                <div id="not-connected-icon-container">
                    <img class="not-connected-icon" :src="getNotConnectedMessage(phoneStore.state).icon" />
                </div>
                <p>{{ getNotConnectedMessage(phoneStore.state).message }}</p>
            </div>
            <div v-else id="no-notifs-container">
                <div id="no-notifs-icon-container">
                    <img class="no-notifs-icon" :src="getNotConnectedMessage('no-notifications').icon" />
                </div>
                <p>{{ getNotConnectedMessage('no-notifications').message }}</p>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, ref, watch } from 'vue'
import PhoneNotification from '../components/PhoneNotification.vue';
import { Phone } from '../types/Phone.interface';
import { NotConnectedDisplay } from '../types/NotConnectedDisplay.interface';
import { Settings } from '../types/Settings.interface';
import { ColorVars, handleIconLumin } from '../utils/theme';
import usbDisabled from '../assets/icons/usb_disabled.svg';
import phoneLock from '../assets/icons/phone_lock.svg';
import bluetoothDisabled from '../assets/icons/bluetooth_disabled.svg';
import mobileDisabled from '../assets/icons/mobile_disabled.svg';
import noNotifs from '../assets/icons/notifications_off.svg';

export default defineComponent({
    components: {
        PhoneNotification
    },
    setup () {
        
        const phoneStore = ref(inject('phoneStore') as Phone);
        const settingsStore = ref(inject('settingsStore') as Settings);

        const androidMessageMap = new Map<string, NotConnectedDisplay>([
            ['disconnected', {message: 'Connect an android device via USB and enable USB debugging to see notifications!', icon: usbDisabled}],
            ['locked', {message: 'Unlock your android device to see notifications!', icon: phoneLock}],
            ['untrusted', {message: 'Always allow USB debugging from this machine to see notifications!', icon: phoneLock}],
            ['no-notifications', {message: `Awaiting new Android notifications...`, icon: noNotifs}]
        ])

        const iosMessageMap = new Map<string, NotConnectedDisplay>([
            ['disconnected', {message: 'Connect an iOS device via bluetooth to see notifications!', icon: bluetoothDisabled}],
            ['no-notifications', {message: `Awaiting new iOS notifications...`, icon: noNotifs}]
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
                    return {message: 'Connect a device to see notifications!', icon: mobileDisabled}
                }
            }
        }

        watch(settingsStore, () => {
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
    justify-content: center;
    grid-template-columns: 70%;
    height: 70vh;
    width: 75%;
    overflow: scroll;
    border-radius: 5vh;
}

#no-show {
    height: 70vh;
    align-items: center;
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