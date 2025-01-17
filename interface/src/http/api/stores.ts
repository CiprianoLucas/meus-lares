import { defineStore } from 'pinia'

type ApiListResponse = {
    results: { [key: string]: string | number | boolean | object | unknown[] | null }[]
    count: number
    next: null | string
    previous: null | string
}

type ApiListCash = {
    createAt: number
    expirate: number
    response: ApiListResponse
}

export const apiListStore = defineStore('apiCash', {
    state: (): { url: string; result: ApiListCash }[] => [],

    actions: {
        setResult(url: string, result: ApiListCash) {
            const unsetOld = this.$state.filter(item => item.url !== url)
            this.$state.splice(0, this.$state.length, ...unsetOld, { url, result })
        },

        getResult(url: string) {
            return this.$state.find(item => item.url === url)?.result || null;
        },

        remove(url: string) {
            const unsetOld = this.$state.filter(item => item.url !== url)
            this.$state.splice(0, this.$state.length, ...unsetOld)
        },

        clear(){
            this.$state.splice(0, this.$state.length)
        }
    },

    persist: {
        enabled: false,
        strategies: [
            {
                key: 'apiCash',
                storage: sessionStorage
            }
        ]
    } as any
})
