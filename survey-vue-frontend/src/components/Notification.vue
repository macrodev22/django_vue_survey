<template>
    <div v-if="notification.show"
    class="fixed bottom-4 left-[50%] translate-x-[-50%] min-w-[400px] py-2 px-4 rounded-md text-white text-center animate-fade-in-down" :class="[notification.type == 'success' ? 'bg-emerald-500' : 'bg-red-500']">
        {{ notification.message }}
    </div>
</template>
<script setup>
import { computed } from 'vue';
import { useStore } from '../store';

const store = useStore()

const notification = computed(() => store.notification)
</script>