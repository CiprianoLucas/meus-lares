<template>
	<div class="container mt-5">
		<h1 class="text-center">Registrar condomínio</h1>
		<custom-form :form="placeForm" :inputs="inputs" />
		<button v-if="!placeId" @click="registerPlace" class="btn btn-primary">Cadastrar</button>
		<div v-else>
			<button @click="updatePlace" class="btn btn-primary mx-3">Atualizar</button>
			<router-link class="btn btn-secondary mx-3" :to="`/condominio/${placeId}/sindicos`">Cadastrar
				síndicos</router-link>
			<router-link class="btn btn-secondary mx-3" :to="`/condominio/${placeId}/moradores`">Cadastrar
				moradores</router-link>
		</div>
	</div>
</template>

<script lang="ts" setup>
import app from '@/app'
import CustomForm from '@/components/forms/CustomForm.vue';
import { inputsProps } from '@/components/forms';
import type { Place } from '../interfaces';

const inputs = app.ref(inputsProps)

const placeId = app.ref(app.routeParam('id'))

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

app.watch(() => placeForm.value.cep, (newValue, oldValue) => {
	verifyCep(newValue)
});

app.watch(() => placeForm.value.state, (newValue, oldValue) => {
	updateCities(newValue)
});

async function updateCities(uf: string = '') {
	const info = await app.api.getCashed('/place/cities/' + uf) as [{ id: number, name: string, state: string }]
	const options = info.map(item => ({ value: item.id, label: item.name }));
	const cityInput = inputs.value.find(input => input.reference === 'city');
	if (cityInput && cityInput.options) {
		cityInput.options = options;
	}
}

async function verifyCep(cep: string = '') {
	if (cep.length === 9) {
		const info = await <Place>app.api.getCashed('/place/cep/' + cep)
		placeForm.value.city = info.city
		placeForm.value.state = info.state
		placeForm.value.neighborhood = info.neighborhood
		placeForm.value.street = info.street
	}
}

function registerPlace() {
	app.api.post('/place/', placeForm.value)
		.then(({ data }) => {
			app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
			sessionStorage.removeItem('/place/unions/')
			app.redirect('/condominio/lista')
		})
		.catch(error => {
			app.popup("Erro!", app.resumeErrors(error), 'warning')
		})
}

function updatePlace() {
	app.api.put(`/place/${placeId.value}/`, placeForm.value)
		.then(() => {
			app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
			sessionStorage.removeItem('/place/unions/')
			app.redirect('/condominio/lista')
		})
		.catch(error => {
			app.popup("Erro!", app.resumeErrors(error), 'warning')
		})
}

app.onMounted(() => {
	if (placeId.value) {
		app.api.get(`/place/${placeId.value}/`)
			.then(response => {
				placeForm.value = response.data
			})
			.catch(() => {
				app.popup('Erro!', 'Falha ao obter informações do condomínio', 'warning')
			})
	}
})

</script>