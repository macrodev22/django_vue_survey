<template>
    <div class="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-md">
      <h1 class="text-2xl font-bold mb-4">User Profile</h1>
      <div class="flex items-center space-x-4">
        <img
          :src="user.imageUrl"
          alt="User Avatar"
          class="h-24 w-24 rounded-full border-2 border-gray-300"
        />
        <div>
          <h2 class="text-xl font-semibold text-gray-500">{{ user.name }}</h2>
          <p class="text-gray-600">{{ user.email }}</p>
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
        <button
          @click="editProfile"
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Edit Profile
        </button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue'
  import { useStore } from '../store'

  const user = useStore().auth.user.data

  const creationTime = computed(() => {
    const date = new Date(user.created_at)

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

  user.imageUrl = 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80'
  </script>
  
  <style scoped>
  /* Add any additional styles here if needed */
  </style>