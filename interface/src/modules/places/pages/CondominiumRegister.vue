<template>
    <div class="container mt-5">
        <h1 class="text-center">Registrar condomínio</h1>
        <custom-form :form="placeForm" :inputs="inputs" />
        <div class="mb-3">
            <label for="user-image-input" class="form-label">Foto de perfil do condomínio:</label>
            <input type="file" class="form-control" id="user-image-input" @change="photoChange" required />
        </div>
        <div class="d-flex justify-content-center mt-5">
            <button @click="registerPlace" class="btn btn-primary">Cadastrar</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomForm from '@/components/forms/CustomForm.vue'
import { inputsProps } from '@/components/forms'
import type { Place } from '../interfaces'

const inputs = app.ref(inputsProps)

const placeForm = app.ref<Place>({
    name: '',
    cep: '',
    number: '',
    street: '',
    complement: '',
    neighborhood: '',
    city: 0,
    state: ''
})

const userImageInput = app.ref<File | null>(null)

async function photoChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0] || null;
    userImageInput.value = file;
};

app.watch(
    () => placeForm.value.cep,
    (newValue, oldValue) => {
        verifyCep(newValue)
    }
)

app.watch(
    () => placeForm.value.state,
    (newValue, oldValue) => {
        updateCities(newValue)
    }
)

async function updateCities(uf: string = '') {
    const { result } = (await app.api.getListCashed('/place/cities/' + uf)) as {
        result: [{ id: number; name: string; state: string }]
    }
    const options = result.map((item) => ({ value: item.id, label: item.name }))
    const cityInput = inputs.value.find((input) => input.reference === 'city')
    if (cityInput && cityInput.options) {
        cityInput.options = options
    }
}

async function verifyCep(cep: string = '') {
    if (cep.length === 9) {
        const {data} = await (app.api.get('/place/cep/' + cep))
        placeForm.value.city = data.city
        placeForm.value.state = data.state
        placeForm.value.neighborhood = data.neighborhood
        placeForm.value.street = data.street
    }
}

function registerPlace() {
    app.api
        .post('/place/condominium/', placeForm.value)
        .then(({ data }) => {
            app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
            sessionStorage.removeItem('/place/condominium/')
            app.redirect('/condominio/lista')
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
}
</script>
