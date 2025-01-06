<template>
    <div class="container d-flex justify-content-center align-items-center">
        <div class="card p-4 shadow-sm" style="max-width: 400px; width: 100%">
            <h2 class="text-center mb-4">Entrar</h2>
            <form @submit.prevent="login">
                <div class="mb-3">
                    <label for="username" class="form-label">Usuário ou e-mail:</label>
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
                <button type="submit" class="btn btn-primary w-100" :disabled="buttonDisabled">
                    Entrar
                </button>
            </form>
            <div id="google-login-button" class="d-flex justify-content-center mt-3"></div>

            <router-link class="text-black text-decoration-none" to="/usuario/cadastro">
                <div class="text-center mt-5 p-2 border rounded">
                    <span>Registre-se</span>
                </div>
            </router-link>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import { userStore } from '@/modules/user/stores'

const user = userStore()

const form = app.ref({
    username: '',
    password: ''
})

const handleGoogleLogin = (token: string) => {
    buttonDisabled.value = true
    app.api
        .post('/user/google-login/', { access_token: token })
        .then(({ data }) => {
            if (!data.has_user) {
                app.redirect({
                    name: 'cadastro_usuario',
                    query: {
                        full_name: data.full_name,
                        email: data.email
                    }
                })
                return
            }
            app.redirect('/')
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
            buttonDisabled.value = false
        })
}

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

const buttonDisabled = app.ref(false)

const login = () => {
    buttonDisabled.value = true
    app.api
        .login(form.value)
        .then(() => {
            switch(user.role){
                case "owner":
                    app.redirect('/proprietario')
                    break
                case "tenant":
                    app.redirect('/morador')
                    break
                case "":
                    app.redirect('/usuario/papel')
                    break
            }
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning')
            buttonDisabled.value = false
        })
}
</script>
