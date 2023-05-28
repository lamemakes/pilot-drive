<template>
    <div v-if="updateHasInfo(updateStore)" class="update-btn-container">
        <div v-if="updateStore.update && !updateStore.update.completed" class="update-btn ready-btn" @click="attemptUpdate">
            <span v-if="!attemptingUpdate">Update to v{{ updateStore.update.version }}</span>
            <span v-else class="dot-loading">
                <div className="dot dot1"></div>
                <div className="dot dot2"></div>
                <div className="dot dot3"></div>
                <div className="dot dot4"></div>
            </span>
        </div>
        <div v-if="updateStore.update && updateStore.update.completed" class="update-btn ready-btn" style="cursor: default;">
            <span>🎉 Updated to v{{ updateStore.update.version }} 🎉</span>
        </div>
        <div v-if="updateStore.error" class="update-btn failed-btn">
            <span>{{ updateStore.error }}</span>
        </div>
    </div>
    <div v-else class="update-btn-container">
        <div class="update-btn check-btn" @click="checkUpdate">
            <span v-if="!checkingUpdate">Check for updates</span>
            <span v-else class="dot-loading">
                <div className="dot dot1"></div>
                <div className="dot dot2"></div>
                <div className="dot dot3"></div>
                <div className="dot dot4"></div>
            </span>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, inject, PropType, ref } from 'vue'
import { Updates } from '../../types/Updates.interface';

export default defineComponent({
    setup () {
        const updateStore = ref(inject("updateStore") as Updates)
        const websocket = ref(inject("websocket") as WebSocket)
        const attemptingUpdate = ref(false)
        const checkingUpdate = ref(false)

        const updateHasInfo = (updateObj: Updates): boolean => {
            if (updateObj.update && updateObj.update.completed) {
                setTimeout(() => updateStore.value = {}, 4000 )
            }
            return (updateObj.error || updateObj.update) ? true : false
        }

        const checkUpdate = () => {
            checkingUpdate.value = true
            websocket.value.send(
                JSON.stringify(
                    {
                        type: "updater",
                        updater: "check" 
                    }
                )
            )
        }

        const attemptUpdate = () => {
            // Send the update instruction to the backend, then attempt to refresh the UI after 5 seconds
            websocket.value.send(
                JSON.stringify(
                    {
                        type: "updater",
                        updater: "update" 
                    }
                )
            )
            attemptingUpdate.value = true
            setTimeout(() => {
                window.location.replace("/");
            }, 5000)
        }

        return {updateStore, attemptingUpdate, checkingUpdate, updateHasInfo, checkUpdate, attemptUpdate}
    }
})
</script>

<style scoped>
@keyframes fadeinout { 
    from { opacity: 1; } to { opacity: 0; }
}

@-webkit-keyframes fadeinout {
    from { opacity: 0; }
    to { opacity: 1; }
}

@-moz-keyframes fadeinout {
    from { opacity: 0; }
    to { opacity: 1; }
}

.update-btn-container {
    width: 100%;
    height: 100%;  
}

.update-btn {
    width: 100%;
    height: 100%;
}

.dot-loading {
    display: flex;
    justify-content: center;
}

.dot { 
    animation: fadeinout 0.5s ease-in alternate infinite;
    -webkit-animation: fadeinout 0.5s ease-in alternate infinite;
    -moz-animation: fadeinout 0.5s ease-in alternate infinite;
    background-color: var(--accent-color);
    border-radius: 50%;
    width: 15px;
    height: 15px;
    margin-left: 10px;
    margin-right: 10px;
}

.dot1 {
    animation-delay: 0;
}

.dot2 {
    animation-delay: .25s;
}

.dot3 {
    animation-delay: .5s;
}

.dot4 {
    animation-delay: .75s;
}
</style>