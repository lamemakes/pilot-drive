<template>
    <div id="notification-container" v-if="notification" :class="(notification.body) ? 'body-notif' : 'no-body-notif'">
        <p id="heading-container" class="notif-text"><span id="title">{{ notification.title }}</span> - <span id="name">{{ notification.app_name }}</span></p>
        <p id="body" class="notif-text" v-if="notification.body">{{ notification.body }}</p>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { PhoneNotification } from '../types/phone.interface'

export default defineComponent({
    props: {
        notification: Object as PropType<PhoneNotification>
    },
    setup (props) {

        const notification = props.notification

        return {notification}
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
    margin: 4px 0px;
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

#title {
    font-size: 18px;
    font-weight: bold;
}

</style>