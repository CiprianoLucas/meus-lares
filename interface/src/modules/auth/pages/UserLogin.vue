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
				<button type="submit" class="btn btn-primary w-100" :disabled="buttonDisabled">Login</button>
			</form>
		</div>
	</div>
</template>

<script lang="ts" setup>
	import app from '@/app'

	const form = app.ref({
		username: '',
		password: '',
	})

	const buttonDisabled = app.ref(false)
	
	const router = app.useRouter();
	const login = () => {
		buttonDisabled.value = true
		app.api.login(form.value)
		.then(()=>{
			router.push('/');
		})
		.catch((error)=>{
			if (error.status == 401){
				app.popup('Falha ao entrar!', 'Usuário ou senha incorretos.', 'warning')
			} else {
				app.popup('Falha ao entrar!', 'Algo não saiu como esperado.', 'warning')
			}

			buttonDisabled.value = false
		})
	}
</script>
