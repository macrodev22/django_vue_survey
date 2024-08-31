<template>
    <div class="p-5 bg-green-500 text-white">
        Survey view
    </div>
</template>

<script setup>
import { onMounted, getCurrentInstance } from 'vue';

const { emit } = getCurrentInstance()

onMounted(() => {
    emit('update-title', 'Surveys')
})

</script>