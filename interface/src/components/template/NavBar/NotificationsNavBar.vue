<template>
    <div v-if="loading" class="d-flex justify-content-center align-items-center p-3">
        <div class="spinner-border text-light" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
    <div v-else class="py-2">
        <div class="d-flex justify-content-between align-items-center mx-3">
            <h4 class="text-center w-100 m-0">Notificações</h4>
            <button @click="getNotifications(true)" type="button" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-clockwise"></i>
            </button>
        </div>
        <div v-for="(notification, index) in notifications" class="bg-dark">
            <div class="pt-2">
                <div
                    :class="`card mx-2 border border-${notification.confirmed_at ? 'secondary' : 'primary'} bg-dark text-light`"
                >
                    <div class="row g-0">
                        <div v-if="notification.image" class="col-2">
                            <img
                                :src="notification.image ?? ''"
                                :alt="notification.title"
                                style="height: 50px"
                                class="img-fluidt rounded-end-0 rounded-top-1"
                            />
                        </div>
                        <div class="col d-flex align-items-center justify-content-center">
                            <div class="text-center">
                                <p class="p-0 m-0">
                                    <small style="font-size: 0.7rem">{{
                                        formatDateTime(notification.schedule)
                                    }}</small>
                                </p>
                                <h5 class="card-title m-0">{{ notification.title }}</h5>
                            </div>
                        </div>

                        <div
                            :class="`col-12 border-top border-${notification.confirmed_at ? 'secondary' : 'primary'}`"
                        >
                            <div class="card-body">
                                <p class="card-text justify-text" style="font-size: 0.85rem">
                                    {{ notification.description }}
                                </p>
                            </div>
                        </div>
                        <div class="row pb-2 m-0">
                            <div class="col-6">
                                <button
                                    v-if="!notification.confirmed_at"
                                    @click="confirmView(index)"
                                    class="btn btn-primary"
                                >
                                    Confirmar
                                </button>
                            </div>
                            <div class="col-6 d-flex justify-content-end">
                                <a
                                    v-if="notification.url"
                                    :href="notification.url"
                                    class="btn btn-secondary"
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    >Acessar</a
                                >
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { api } from '@/http'
import app from '@/app'
import { ref, onMounted, onBeforeUnmount, watch, computed } from 'vue'

interface Notification {
    id: string
    title: string
    description: string
    schedule: string
    url: string | null
    image: string | null
    confirmed_at: string | null
}

const notifications = ref<Notification[]>([])
const loading = ref<boolean>(true)

function formatDateTime(isoString: string): string {
    const date = new Date(isoString)
    return date.toLocaleString('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    })
}

function confirmView(index: number) {
    const notification = notifications.value[index]
    api.post('/notification/confirm/', { id: notification.id })
        .then(() => {
            notification.confirmed_at = 'confirmed'
        })
        .catch(() => {
            app.popup('Falha ao confirmar', '', 'warning')
        })
}

function getNotifications(force?: boolean) {
    api.getListCashed('/notification/main/', force)
        .then(({ result }) => {
            notifications.value = result as Notification[]
            notifications
        })
        .catch((error) => {})
        .finally(() => {
            loading.value = false
        })
}

onMounted(() => {
    getNotifications()
})
</script>
