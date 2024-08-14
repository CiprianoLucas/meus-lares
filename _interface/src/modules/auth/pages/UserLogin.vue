<template>
	<div class="container d-flex justify-content-center align-items-center min-vh-100">
		<div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%">
			<h2 class="text-center mb-4">Login</h2>
			<form @submit.prevent="login">
				<div class="mb-3">
					<label for="email" class="form-label">Email:</label>
					<input
						type="email"
						id="email"
						v-model="form.email"
						required
						class="form-control"
						placeholder="Digite seu email"
					/>
				</div>
				<div class="mb-3">
					<label for="password" class="form-label">Password:</label>
					<input
						type="password"
						id="password"
						v-model="form.password"
						required
						class="form-control"
						placeholder="Digite sua senha"
					/>
				</div>
				<button type="submit" class="btn btn-primary w-100">Login</button>
			</form>
		</div>
	</div>
</template>

<script lang="ts" setup>
	import { ref } from 'vue'
	import { api } from '@/http'

	const form = ref({
		email: 'admin@admin.com',
		password: 'admin',
	})

	const login = () => {
		api.login(form.value)
	}
</script>
