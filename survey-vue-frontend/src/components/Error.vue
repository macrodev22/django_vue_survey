<template>
    <div v-if="errorMsg" class="flex items-center justify-between py-3 px-5 bg-red-500 rounded text-white">
        {{ errorMsg }}
        <span @click="() => emit('close-message')"
            class="flex items-center justify-center w-8 h-8 rounded-full transition-colors hover:bg-[rgba(0,0,0,0.2)] cursor-pointer">
            <XMarkIcon class="w-6" />
        </span>
    </div>
</template>
<script setup>
import { defineProps, defineEmits } from 'vue';
import { XMarkIcon } from '@heroicons/vue/24/outline'

const props = defineProps({
    errorMsg: String,
})

const emit = defineEmits(['close-message'])

</script>