import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import { createPinia } from 'pinia'
import router from './router'

// Tailwind
import './input.css'

const pinia = createPinia()
pinia.use(({store}) => {
    store.$subscribe((mutation, state) => {
        localStorage.setItem('surveys',JSON.stringify(state.surveys))
    })
})

createApp(App)
    .use(pinia)
    .use(router)
    .mount('#app')
