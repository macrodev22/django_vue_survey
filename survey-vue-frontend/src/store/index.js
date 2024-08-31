import { defineStore } from "pinia";

export const useStore = defineStore('store', {
    state: () => {
        return {
            suveys: [],
            auth: {
                user: {
                    data: JSON.parse(sessionStorage.getItem("USER")) || {},
                    token: JSON.parse(sessionStorage.getItem("TOKEN")) || null
                }
            }
        }
    },
    actions: {
        logout() {
            this.auth.user.token = null
            sessionStorage.removeItem("TOKEN")
            sessionStorage.removeItem("USER")
            return Promise.resolve()
        },
        login(user, token) {
            this.auth.user.token = token
            this.auth.user.data = user

            sessionStorage.setItem("TOKEN", JSON.stringify(token))
            sessionStorage.setItem("USER", JSON.stringify(user))
        }
    },
    getters: {

    }
})