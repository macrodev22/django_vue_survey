<template>
  <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
    <h1 class="text-2xl font-bold mb-4 text-gray-600">User Profile</h1>
    <div class="flex items-center space-x-4">
      <img :src="user.imageUrl" alt="User Avatar" class="h-24 w-24 rounded-full border-2 border-gray-300" />
      <div>
        <h2 class="text-xl font-semibold text-gray-500">{{ user.name }}</h2>
        <p class="text-gray-600">{{ user.email }}</p>
      </div>
      <div class="ml-5 flex flex-col gap-5 items-center">
        <button type="button"
          class="relative rounded-md bg-white px-2.5 py-1.5 text-sm font-semibold text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 hover:bg-gray-50">
          <input type="file" @change="imageChanged" name="survey-image" accept="image/*"
            class="absolute left-0 top-0 top-0 bottom-0 opacity-0 cursor-pointer">
          Change
        </button>
        <button type="button" @click="revertImage"
          class="flex items-center justify-center rounded-full w-10 h-10 border hover:bg-gray-50">
          <ArrowPathIcon class="w-7 h-7" style="color: black;" />
        </button>
      </div>
    </div>
    <div class="mt-6">
      <h3 class="text-lg font-semibold">About Me</h3>
      <p class="text-gray-700">{{ user.bio }}</p>
    </div>
    <div class="mt-6">
      <h3 class="text-lg font-semibold text-gray-600 border-t border-gray-300 pb-4">Other Information</h3>
      <p class="text-gray-700">Is staff: {{ user.is_staff }}</p>
      <p class="text-gray-700">Created at: {{ creationTime }}</p>
    </div>
    <div class="mt-6">
      <button @click="updateProfile" class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700">
        Update Profile
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useStore } from '../store'

import { ArrowPathIcon } from '@heroicons/vue/24/outline';

const store = useStore()
const user = computed(() => store.auth.user.data)

const creationTime = computed(() => {
  const date = new Date(store.auth.user.data.created_at)

  const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short',
  };

  const formatter = new Intl.DateTimeFormat('en-US', options);

  // Format the date
  const formattedDate = formatter.format(date);

  return formattedDate
})

const revertImage = () => {
  store.auth.user.data.imageUrl = store.auth.user.data.image
}

const imageChanged = (event) => {
  const file = event.target.files[0]

  const reader = new FileReader()
  reader.onloadend = () => {
    store.auth.user.data.imageUrl  = reader.result
  }

  reader.readAsDataURL(file)

}

const updateProfile = () => {
  store.updateUser()
}

</script>

<style scoped>
/* Add any additional styles here if needed */
</style>