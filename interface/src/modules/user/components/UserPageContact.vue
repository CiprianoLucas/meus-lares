<template>
    <div class="d-flex justify-content-between pb-3">
        <h3 class="p-0 m-0">Contatos</h3>
        <button
            @click="changeEditMode"
            to="/usuario/edicao/documentos"
            :class="`py-0 btn btn-${editMode ? 'primary' : 'secondary'}`"
        >
            <small v-if="editMode">Salvar</small>
            <small v-else>Editar</small>
        </button>
        <button v-if="editMode" @click="editMode = false" class="btn btn-secondary">
            Cancelar
        </button>
    </div>
    <div v-if="editMode">
        <text-input
            label="Como quer ser chamado:"
            type="text"
            id="nick"
            v-model="contactForm.nick"
        />
        <text-input
            label="Telefone:"
            type="text"
            id="phone"
            mask="(##) #####-####"
            v-model="contactForm.phone_number"
        />
        <text-input label="Email:" type="text" id="email" v-model="user.email" disabled />
    </div>
    <div v-else class="user-info-card">
        <dl>
            <dt>Como quer ser chamado:</dt>
            <dd>{{ user?.nick }}</dd>
            <dt>Telefone:</dt>
            <dd>{{ user?.phone_number }}</dd>
            <dt>E-mail:</dt>
            <dd>{{ user?.email }}</dd>
        </dl>
    </div>
</template>

<script setup lang="ts">
import app from '@/app'
import type { User } from '../interfaces'
import TextInput from '@/components/forms/TextInput.vue'

const props = defineProps<{
    user: User
    update: Function
}>()

const contactForm = app.ref<User>({})
const editMode = app.ref(false)

function changeEditMode() {
    editMode.value = !editMode.value
    if (!editMode.value) {
        saveContacts()
        return
    }
    contactForm.value.nick = props.user.nick
    contactForm.value.phone_number = props.user.phone_number
}

function saveContacts() {
    app.loading(true)
    app.api
        .patch('/user/profile/' + props.user.id + '/', contactForm.value)
        .then(() => {
            props.update()
            app.popup('Atualizado!', 'Contatos atualizados com sucesso')
        })
        .catch((error) => {
            editMode.value = true
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}
</script>
