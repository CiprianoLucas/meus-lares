<template>
    <div class="container mt-5">
        <h1 class="text-center">Registrar condomínio</h1>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { inputsProps } from '@/components/forms'
import type { Place } from '../interfaces'

const inputs = app.ref(inputsProps)

const placeId = app.ref(app.routeParam('id'))

const userImageInput = app.ref<File | null>(null)

async function photoChange(event: Event) {
    const target = event.target as HTMLInputElement;
    const file = target.files?.[0] || null;
    userImageInput.value = file;
};

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

function updatePlace() {
    app.api
        .put(`/place/${placeId.value}/`, "placeForm.value")
        .then(() => {
            app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
            sessionStorage.removeItem('/place/condominium/')
            app.redirect('/condominio/lista')
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
        })
}

app.onMounted(() => {
    if (placeId.value) {
        app.api
            .get(`/place/condominium/${placeId.value}/`)
            .then((response) => {
            })
            .catch(() => {
                app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
            })
    }
})
</script>
