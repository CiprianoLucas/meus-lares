import { defineStore } from 'pinia'

interface LoadingPageState {
    message: string
    show: boolean
}

export const loagingPageStore = defineStore('loadingPage', {
    state: (): LoadingPageState => ({
        message: 'Carregando...',
        show: false
    }),
    actions: {
        loading(show: boolean, message: string = 'Carregando...') {
            this.$state.message = message
            this.$state.show = show
        }
    }
})
