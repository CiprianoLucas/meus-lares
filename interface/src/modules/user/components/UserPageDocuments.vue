<template>
    <div class="d-flex justify-content-between pb-3">
        <h3 class="p-0 m-0"> Documentos</h3>
        <button v-if="user?.verified_status == 'pending' || user?.verified_status == 'rejected'" @click="changeEditMode"
            to="/usuario/edicao/documentos" :class="`py-0 btn btn-${editMode ? 'primary' : 'secondary'}`">
            <small v-if="editMode">Salvar</small>
            <small v-else>Editar</small>
        </button>
    </div>
    <div v-if="editMode">
        <text-input label="Nome completo: (sem abreviatura)" type="text" id="full_name" v-model="documentForm.full_name"
            required />
        <text-input label="CPF:" :validators="[verifyCpf]" type="text" id="cpf" mask="###.###.###-##"
            v-model="documentForm.cpf" required />
        <text-input label="Data de nascimento:" :validators="[verifyDate]" placeholder="dd/mm/aaaa" type="text"
            id="birth" mask="##/##/####" v-model="documentForm.birth" required />
    </div>
    <div v-else class="user-info-card mb-3">
        <dl>
            <dt>Nome completo:</dt>
            <dd>{{ user?.full_name }}</dd>
            <dt>CPF:</dt>
            <dd>{{ user?.cpf }}</dd>
            <dt>Data de nascimento:</dt>
            <dd>{{ user?.birth }}</dd>
            <dt>Verificação de identidade:</dt>
            <dd>{{ verifiedStatusMap[user?.verified_status || "pending"] }}</dd>
        </dl>
        <div class="d-flex justify-content-center">
        </div>
    </div>
    <div v-if="['pending', 'rejected'].includes(user.verified_status || '') && !editMode">
        <div class="d-flex justify-content-center pb-3">
            <h6 class="p-0 m-0"> Faça a verificação </h6>
        </div>
        <file-input id="file-document" label="Frente do documento de identidade"
            v-model="verificationForm.document_front_photo" class="mb-3"/>
        <file-input id="file-document" label="Verso do documento de identidade"
            v-model="verificationForm.document_back_photo" class="mb-3"/>
        <file-input id="file-document" label="Foto do rosto" v-model="verificationForm.self_photo" class="mb-3" />
        <file-input id="file-document" label="Foto do rosto com documento de identidade ao lado" class="mb-3"
            v-model="verificationForm.self_with_document_photo" />
        <div class="d-flex justify-content-center">
            <button @click="startVerification" class="btn btn-primary">Iniciar verificação</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import app from '@/app'
import type { User } from '../interfaces'
import { verifiedStatusMap } from '../interfaces';
import { verifyDate, verifyCpf } from '@/components/validators';
import TextInput from '@/components/forms/TextInput.vue';
import FileInput from '@/components/forms/FileInput.vue';
import { objectToFormData } from '@/components/formaters';

const props = defineProps<{
    user: User
    update: Function
}>()

const documentForm = app.ref<User>({})
const verificationForm = app.ref({
    document_front_photo: null as File | null,
    document_back_photo: null as File | null,
    self_photo: null as File | null,
    self_with_document_photo: null as File | null,
})
const editMode = app.ref(false)

function changeEditMode() {
    editMode.value = !editMode.value
    if (!editMode.value) {
        saveDocuments()
        return
    }
    documentForm.value.birth = props.user.birth
    documentForm.value.cpf = props.user.cpf
    documentForm.value.full_name = props.user.full_name
}

function startVerification() {
    if(
        !verificationForm.value.document_front_photo ||
        !verificationForm.value.document_back_photo ||
        !verificationForm.value.self_photo ||
        !verificationForm.value.self_with_document_photo
    ){
        app.popup("Erro!", "Insira todos os documentos solicitados", "warning")
        return
    }
    app.loading(true)
    const payload = objectToFormData(verificationForm.value)
    app.api
        .patch('/user/profile/' + props.user.id + '/', payload)
        .then(({ data }) => {
            props.update()
        })
        .catch((error) => {
            editMode.value = true
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

function saveDocuments() {
    app.loading(true)
    app.api
        .patch('/user/profile/' + props.user.id + '/', documentForm.value)
        .then(({ data }) => {
            props.update()
        })
        .catch((error) => {
            editMode.value = true
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
        .finally(() => {
            app.loading(false)
        })
}

app.onMounted(() => {
})
</script>

<style></style>
