<template>
    <div id="notification-container" v-if="notification" :class="(hasBody) ? 'body-notif' : 'no-body-notif'">
        <p id="heading-container" class="notif-text"><span id="name">{{ notification.app_name }}</span> - <span id="title">{{ notification.title }}</span></p>
        <p id="body" class="notif-text" v-if="hasBody">{{ notification.body }}</p>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { PhoneNotification } from '../types/Phone.interface'

export default defineComponent({
    props: {
        notification: Object as PropType<PhoneNotification>
    },
    setup (props) {

        const notification = props.notification

        const hasBody = notification?.body && notification?.body != "null"  // Sometimes null is returned as a string

        return {notification, hasBody}
    }
})
</script>

<style scoped lang="scss">
#notification-container {
    background-color: var(--secondary-color);
    color: var(--secondary-lumin);
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
    margin: 6px 0px;
    box-shadow: 0.5rem 0.5rem black;
    border-radius: 5vh;
    p {
        margin: 0px 15px;
    }
}

.body-notif {
    height: 15vh;
}

.no-body-notif {
    height: 10vh;
}

#heading-container {
    margin: 0px
}

#name{
    font-size: 18px;
    font-weight: bold;
}

</style>