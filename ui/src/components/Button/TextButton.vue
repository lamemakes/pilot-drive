<template>
    <div class="text-btn">
        <p>{{buttonText}}</p>
    </div>
</template>

<script lang="ts">
import { defineComponent, toRef } from 'vue'

export default defineComponent({
    props: {
        text: String,
    },
    setup (props) {
        const buttonText = toRef(props, "text")

        return {buttonText}
    }
})
</script>

<style scoped>

</style>