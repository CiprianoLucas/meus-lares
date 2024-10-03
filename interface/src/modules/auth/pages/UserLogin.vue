<template>
	<div class="container d-flex justify-content-center align-items-center min-vh-100">
		<div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%">
			<h2 class="text-center mb-4">Login</h2>
			<form @submit.prevent="login">
				<div class="mb-3">
					<label for="username" class="form-label">Nome de usuário:</label>
					<input
						type="text"
						id="username"
						v-model="form.username"
						required
						class="form-control"
						placeholder="Digite seu nome de usuário"
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
	import { useRouter } from 'vue-router';
	import { api } from '@/http'

	const form = ref({
		username: 'admin',
		password: 'admin',
	})

	const router = useRouter();
	const login = () => {
		api.login(form.value)
		.then(()=>{
			router.push('/');
		})
	}
</script>
