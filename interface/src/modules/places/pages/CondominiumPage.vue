<template>
    <div v-if="condominium.id">
        <div class="border-bottom d-flex flex-column justify-content-center align-items-center py-2">
            <h2>{{ condominium.name }}</h2>
            <img v-if="condominium.profile_photo" :src="condominium.profile_photo" class="condominium-img"
                alt="foto do condomínio">
            <button @click="triggerFileInput" class="btn btn-secondary py-0 my-1"><small>Alterar foto do
                    condominio</small></button>
            <input ref="fileInputRef" type="file" @change="photoChange" style="display: none;" />
        </div>
        <div class="border-bottom px-4 py-3">
            <div class="d-flex justify-content-between mb-3">
                <h3 class="p-0 m-0">Localização:</h3>
                <router-link :to="'/condominio/edicao/' + condominiumId"
                    class="btn btn-secondary py-0"><small>Editar</small></router-link>
            </div>
                <p>{{ `${condominium.street}, ${condominium.number}` }}</p>
                <p>{{ `${condominium.neighborhood}, ${condominium.city_name}` }}</p>
                <p>{{ `${condominium.state}, ${condominium.cep}, ${condominium.complement}` }}</p>
        </div>
        <div class="border-bottom px-4 pt-2 pb-5 mb-3">
            <collapse-apartments :condominiumId="condominiumId" />
        </div>
        <div class="border-bottom px-4 pt-2 pb-5">
            <collapse-parks :condominiumId="condominiumId" />
        </div>
        <div class="border-bottom px-4 pt-2 pb-5">
            <collapse-shared-places :condominiumId="condominiumId" />
        </div>
        <div class="border-bottom px-4 pt-2 pb-5">
            <div class="d-flex justify-content-center my-2">
                <button class="btn btn-secondary py-2 px-3 w-100" type="button">
                    Moradores
                </button>
            </div>
        </div>
        <div class="d-flex justify-content-center border-bottom px-4 pt-2 pb-5">
            <button class="btn btn-danger py-1">Excluir</button>
        </div>
    </div>
    <div v-else>
        <div class="d-flex justify-content-center border-bottom px-4 py-3">
            <p class="text-center">Falha ao obter informações do condominio.</p>
        </div>
        <div class="d-flex justify-content-center border-bottom px-4 py-3">
            <button @click="goBack" class="btn btn-secondary py-1">Voltar</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import type { Condominium } from '../interfaces'
import collapseApartments from '../components/collapseApartments.vue'
import collapseParks from '../components/collapseParks.vue'
import collapseSharedPlaces from '../components/collapseSharedPlaces.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const condominiumId = app.ref<string>(app.routeParam('id').toString())
const condominium = app.ref<Condominium>({})

const userImageInput = app.ref<File | null>(null)

const fileInputRef = app.ref<HTMLInputElement | null>(null)

function triggerFileInput() {
    fileInputRef.value?.click()
}

async function photoChange(event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0] || null
    userImageInput.value = file

    if (file) {
        const formData = new FormData()
        formData.append('profile_photo', file)
        app.api.patch('/place/condominium/' + condominiumId.value + '/', formData)
            .then(() => {
                getCondominiumValues()
                app.api.removeListCash('/place/condominium/')
                app.popup("Sucesso!", 'Foto de perfil atualizada com sucesso!', 'success')
            })
            .catch(({ error }) => {
                app.popup('Erro ao enviar o arquivo.', error, 'danger')

            })
    }
}

app.onMounted(async () => {
    await getCondominiumValues()
})

function goBack() {
  router.go(-1)
}

async function getCondominiumValues() {
    app.loading(true)
    app.api
        .get(`/place/condominium/${condominiumId.value}/`)
        .then(({ data }) => {
            condominium.value = data
            condominium.value.cep = data.cep.replace(/(\d{5})(\d{3})/, "$1-$2")
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
        })
        .finally(()=>{
            app.loading(false)
        })
}
</script>
<style>
.condominium-img {
    max-width: 200px;
    max-height: 300px;
    width: auto;
    height: auto;
    object-fit: contain;
    border: 1px solid rgb(88, 88, 88);
    border-radius: 20px;
}
</style>