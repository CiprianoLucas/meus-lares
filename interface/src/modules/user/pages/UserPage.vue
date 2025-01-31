<template>
    <div class="container mt-2">
        <h2 class="text-center mb-3">Meu usuário</h2>
        <div class="border-bottom d-flex flex-column justify-content-center align-items-center py-2">
            <img v-if="user?.profile_photo" :src="user.profile_photo" alt="foto de perfil do usuário" class="user-img"/>
            <button @click="triggerFileInput" class="btn btn-secondary py-0 my-1">
                <small>Alterar foto de perfil</small>
            </button>
            <input ref="fileInputRef" type="file" @change="photoChange" style="display: none" />
        </div>
        <div class="border-top py-3">
            <user-page-documents :user="user" :update="getUserValues"/>
        </div>
        <div class="border-top py-3">
            <div class="d-flex justify-content-between pb-3">
                <h3 class="p-0 m-0"> Contatos</h3>
                <router-link to="/usuario/edicao/contatos"
                    class="btn btn-secondary py-0"><small>Editar</small></router-link>
            </div>
            <div class="user-info-card">
                <dl>
                    <dt>Como quer ser chamado:</dt>
                    <dd>{{ user?.nick }}</dd>
                    <dt>Telefone:</dt>
                    <dd>{{ user?.phone_number }}</dd>
                    <dt>E-mail:</dt>
                    <dd>{{ user?.email }}</dd>
                </dl>
            </div>
        </div>

    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { type User } from '../interfaces';
import { userStore } from '../stores';
import { formatCPF, formatDate, formatPhoneNumber } from '@/components/formaters';
import UserPageDocuments from '../components/UserPageDocuments.vue';

const userStoreValues = userStore()
const user = app.ref<User>({id: userStoreValues.id})
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
        app.api
            .patch('/user/profile/' + userStoreValues.id + '/', formData)
            .then(() => {
                getUserValues()
                app.popup('Sucesso!', 'Foto de perfil atualizada com sucesso!', 'success')
            })
            .catch(({ error }) => {
                app.popup('Erro ao enviar o arquivo.', error, 'danger')
            })
    }
}

async function getUserValues() {
    app.loading(true)
    app.api
        .get('/user/profile/' + userStoreValues.id + '/')
        .then(({ data }) => {
            user.value = data as User
            user.value.cpf = formatCPF(user.value?.cpf)
            user.value.birth = formatDate(user.value?.birth)
            user.value.phone_number = formatPhoneNumber(user.value?.phone_number)
        })
        .catch(() => {
            app.popup('Erro!', 'Falha ao obter informações do usuário', 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

app.onMounted(async () => {
    getUserValues()
})
</script>
<style>
.user-img {
    max-width: 200px;
    max-height: 300px;
    width: auto;
    height: auto;
    object-fit: contain;
    border: 1px solid rgb(88, 88, 88);
    border-radius: 20px;
}
</style>