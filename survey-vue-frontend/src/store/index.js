import { defineStore } from "pinia";

export const useStore = defineStore('store', {
    state: () => {
        return {
            suveys: [],
            auth: {
                user: {
                    data: {},
                    token: 'null'
                }
            }
        }
    },
    actions: {

    },
    getters: {

    }
})