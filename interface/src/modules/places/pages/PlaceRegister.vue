<template>
	<div class="container mt-5">
		<h1 class="text-center">Registrar condomínio</h1>
		<custom-form :form="placeForm" />
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

const placeId = app.ref(app.routeParam('id'))

const placeForm = app.ref({
	name: '',
	number: '',
	street: '',
	city: '',
	state: ''
})

function registerPlace() {
	app.api.post('/place/', placeForm.value)
		.then(({ data }) => {
			app.popup('Sucesso!', 'Informações do condomínio salvas', 'success')
			debugger
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