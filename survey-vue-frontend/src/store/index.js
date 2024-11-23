import { defineStore } from "pinia";
import apiClient from "../services/apiClient";

export const useStore = defineStore('store', {
    state: () => {
        return {
            surveys:  JSON.parse(localStorage.getItem('surveys')) || [],
            notification: { show: false, message: '', type: null  },
            auth: {
                user: {
                    data: JSON.parse(sessionStorage.getItem("USER")) || {},
                    token: JSON.parse(sessionStorage.getItem("TOKEN")) || null,
                    refresh: JSON.parse(sessionStorage.getItem("REFRESH")) || null,
                }
            },
            questionTypes: [
                { name: 'Checkbox', type: 'checkbox' },
                { name: 'Single choice', type: 'radio' },
                { name: 'Selection', type: 'select' },
                { name: 'Long text', type: 'textarea' },
                { name: 'Text', type: 'text' },

            ],
            trash: {
                surveys: [],
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
        login(user, token, refresh) {
            this.auth.user.token = token
            this.auth.user.refresh = refresh
            this.auth.user.data = user
            this.auth.user.data.imageUrl = this.auth.user.data.image

            sessionStorage.setItem("TOKEN", JSON.stringify(token))
            sessionStorage.setItem("USER", JSON.stringify(user))
            sessionStorage.setItem("REFRESH", JSON.stringify(refresh))
        },
        deleteSurvey(id) {
            return apiClient.delete(`/surveys/${id}`)
                .then(({ data }) => {
                    this.trash.surveys.push(data)
                    return apiClient.get('/surveys')
                })
                .then(({ data }) => {
                    this.surveys = data
                    return Promise.resolve()
                })
                .catch(err => {
                    console.error(err)
                    return Promise.reject(err)
                })
        },
        updateUser() {
            const userId = this.auth.user.data.id
            this.auth.user.data.image = this.auth.user.data.imageUrl
            const payload = { ...this.auth.user.data }
            delete payload.imageUrl
            apiClient.put(`/users/${userId}`, payload)
            .then(({ data }) => {
                this.auth.user.data = data
                this.auth.user.data.imageUrl = data.image
            })
        },
        notify({ message, type = null }) {
            setTimeout(() => this.notification.show = false, 3000)
            this.notification.message = message
            this.notification.type = type
            this.notification.show = true
        }
    },
    getters: {
        getSurvey(state) {
            return (id) => state.surveys.find(s => s.id == id)
        },
    }
})