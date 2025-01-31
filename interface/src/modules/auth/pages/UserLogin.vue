<template>
    <div class="container d-flex justify-content-center align-items-center">
        <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%">
            <h2 class="text-center mb-4">Entrar</h2>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="email" class="form-label">E-mail:</label>
                    <input
                        type="text"
                        id="email"
                        v-model="form.email"
                        required
                        class="form-control"
                        placeholder="Digite seu e-mail"
                    />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Senha:</label>
                    <input
                        type="password"
                        id="password"
                        v-model="form.password"
                        required
                        class="form-control"
                        placeholder="Digite sua senha"
                    />
                </div>
                <button type="submit" class="btn btn-primary w-100 mt-4" :disabled="buttonDisabled">
                    Entrar
                </button>
            </form>
            <div id="google-login-button" class="d-flex justify-content-center mt-3"></div>
            <a class="d-flex justify-content-center mt-3" :href="passwordChangLink">
                Redefinir minha senha
            </a>

            <router-link class="btn btn-secondary mt-5" to="/usuario/cadastro">
                Cadastre-se
            </router-link>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { userStore } from '@/modules/user/stores'
import { useRouter } from 'vue-router'

const user = userStore()
const router = useRouter()

const form = app.ref({
    email: '',
    password: ''
})

const buttonDisabled = app.ref(false)
const passwordChangLink = app.ref(import.meta.env.VITE_API_URL + '/user/f/password/reset/')

app.onMounted(() => {
    const googleScript = document.createElement('script')
    googleScript.src = 'https://accounts.google.com/gsi/client'
    googleScript.async = true
    googleScript.onload = () => {
        ;(window as any).google.accounts.id.initialize({
            client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
            callback: (response: { credential: string }) => {
                handleGoogleLogin(response.credential)
            }
        })
        ;(window as any).google.accounts.id.renderButton(
            document.getElementById('google-login-button'),
            {
                theme: 'outline',
                size: 'large',
                width: '100%'
            }
        )
    }
    document.head.appendChild(googleScript)
})

const handleGoogleLogin = (token: string) => {
    buttonDisabled.value = true
    app.loading(true, "Entrando...")
    app.api
        .post('/user/google-login/', { access_token: token })
        .then(({ data }) => {
            if (!data.has_user) {
                router.push({
                    name: 'cadastro_usuario',
                    query: {
                        full_name: data.full_name,
                        email: data.email
                    }
                })
                return
            }
            user.id = data.id
            user.roles = data.roles
            if (!user.roles.includes(user.role)) {
                app.api.clearCash()
                user.role = ''
            }
            redirectRole()
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
            buttonDisabled.value = false
        })
        .finally(()=>{app.loading(false)})
}

const login = () => {
    app.loading(true, "Entrando...")
    buttonDisabled.value = true
    app.api
        .login(form.value)
        .then(() => {
            redirectRole()
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
            buttonDisabled.value = false
        })
        .finally(()=>{app.loading(false)})
}

const redirectRole = () => {
    switch (user.role) {
        case 'owner':
            router.push('/proprietario')
            break
        case 'tenant':
            router.push('/morador')
            break
        case '':
            router.push('/usuario/papel')
            break
    }
}
</script>
