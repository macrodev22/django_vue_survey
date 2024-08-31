<template>
    <div class="flex min-h-full flex-1 flex-col justify-center px-6 py-12 lg:px-8">
      <div class="sm:mx-auto sm:w-full sm:max-w-sm">
        <img class="mx-auto h-10 w-auto" src="https://tailwindui.com/img/logos/mark.svg?color=indigo&shade=600" alt="Your Company" />
        <h2 class="mt-10 text-center text-2xl font-bold leading-9 tracking-tight text-gray-900">Sign in to your account</h2>
      </div>
  
      <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
        <form class="space-y-6" action="#" method="POST" @submit.prevent="loginUser">
          <div v-if="errorMsg" class="flex items-center justify-between py-3 px-5 bg-red-500 text-white rounded">{{ errorMsg }}  
            <span class="p-3 cursor-pointer rounded-full hover:bg-[rgba(0,0,0,0.2)]" @click="() => errorMsg=''">X</span>
          </div>
          <div>
            <label for="email" class="block text-sm font-medium leading-6 text-gray-900">Email address</label>
            <div class="mt-2">
              <input id="email" name="email" type="email" v-model="form.email" autocomplete="email" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
            </div>
          </div>
  
          <div>
            <div class="flex items-center justify-between">
              <label for="password" class="block text-sm font-medium leading-6 text-gray-900">Password</label>
              <div class="text-sm">
                <a href="#" class="font-semibold text-indigo-600 hover:text-indigo-500">Forgot password?</a>
              </div>
            </div>
            <div class="mt-2">
              <input id="password" name="password" type="password" v-model="form.password" autocomplete="current-password" required="" class="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6" />
            </div>
          </div>
  
          <div>
            <button type="submit" class="relative flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"> 
              <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                <LockClosedIcon
                  class="h-5 w-5 text-indigo-500 group-hover:text-indigo-400"
                  aria-hidden="true"
                />
              </span>
              Sign in
            </button>
          </div>
        </form>
  
        <p class="mt-10 text-center text-sm text-gray-500">
          Not a member?
          {{ ' ' }}
          <RouterLink to="/register" class="font-semibold leading-6 text-indigo-600 hover:text-indigo-500">Register</RouterLink>
        </p>
      </div>
    </div>
  </template>

<script setup>
import { LockClosedIcon } from '@heroicons/vue/24/outline';
import { RouterLink, useRouter } from 'vue-router';
import { useStore } from '../store'
import { reactive,ref } from 'vue'
import apiClient from '../services/apiClient';

const form = reactive({
  email: '',
  password: ''
})

const errorMsg = ref('')

const store = useStore()
const router = useRouter()

const loginUser = () => {
  apiClient.post('/login', form).then(res => {
    const { data : { user, token } } = res

    store.login(user, token)
    router.replace({ name: 'Dashboard' })
  })
  .catch(err => {

    const { response: { data : { message } } } = err

    errorMsg.value = message
  })
}

</script>
  