<template>
    <div class="container mt-5">
        <h2 class="text-center mb-3">Cadastre-se</h2>
        <text-input label="E-mail:" type="email" id="email" v-model="userForm.email" required />
        <text-input
            label="CPF:"
            type="text"
            id="cpf"
            mask="###.###.###-##"
            v-model="userForm.cpf"
            required
        />
        <text-input
            label="Telefone:"
            type="text"
            id="phone_number"
            mask="(##) ####-#####"
            v-model="userForm.phone_number"
            required
        />
        <text-input
            label="Nome completo: (sem abreviatura)"
            type="text"
            id="full_name"
            v-model="userForm.full_name"
            required
        />
        <text-input
            label="Como quer ser chamado:"
            type="text"
            id="nick"
            v-model="userForm.nick"
            required
        />
        <text-input
            label="Data de nascimento:"
            :validators="[verifyDate]"
            placeholder="dd/mm/aaaa"
            type="text"
            id="birth"
            mask="##/##/####"
            v-model="userForm.birth"
            required
        />
        <text-input
            label="Senha:"
            :type="showPassword ? 'text' : 'password'"
            :buttomLabel="buttonShowPassword"
            :buttomFunction="changeShowPassword"
            :validators="[isPasswordValid]"
            id="password"
            v-model="userForm.password"
            required
            @input="checkPasswordStrength"
        />
        <div class="password-strength mt-2">
            <div :class="strengthPassword" class="password-strength-bar"></div>
        </div>
        <div class="mt-3">
            <span
                v-if="
                    !(
                        (passwordValid && !userForm.password) ||
                        (!passwordValid && userForm.password)
                    )
                "
                >Falta em sua senha:</span
            >
            <ul>
                <li v-if="!hasLowercase">Letra minúscula</li>
                <li v-if="!hasUppercase">Letra maiúscula</li>
                <li v-if="!hasNumber">Número</li>
                <li v-if="!hasSpecialChar">Caractere especial</li>
                <li v-if="!userForm.password">8 caracteres</li>
                <li v-if="userForm.password && userForm.password.length < 8">8 caracteres</li>
            </ul>
        </div>

        <div class="mb-3">
            <text-input
                label="Repita a senha"
                type="password"
                id="repeatPassword"
                v-model="repeatPassword"
                required
                :validators="[passwordRepeatValid]"
            />
        </div>

        <div class="d-flex justify-content-center mt-5">
            <button @click="RegisterUser" class="btn btn-primary" :disabled="registrando">
                Cadastrar
            </button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import app from '@/app'
import type { User } from '../interfaces'
import { computed } from 'vue'
import TextInput from '@/components/forms/TextInput.vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const fullName = String(app.routeQuery('full_name') || '')
const email = String(app.routeQuery('email') || '')
const passwordStrength = app.ref('')
const strengthPassword = app.ref('')
const repeatPassword = app.ref('')
const hasUppercase = app.ref(false)
const hasNumber = app.ref(false)
const hasSpecialChar = app.ref(false)
const hasLowercase = app.ref(false)
const registrando = app.ref(false)
const showPassword = app.ref(false)
const buttonShowPassword = app.ref('<i class="bi bi-eye"></i>')

function changeShowPassword() {
    showPassword.value = !showPassword.value
}

function isPasswordValid() {
    return Boolean(userForm.value.password) && strengthPassword.value !== 'excellent' ? true : false
}

const passwordValid = computed(() => {
    return isPasswordValid()
})

function passwordRepeatValid() {
    return repeatPassword.value != userForm.value.password ? 'Senhas não conferem' : false
}

const userForm = app.ref<User>({
    nick: '',
    email: email,
    cpf: '',
    phone_number: '',
    full_name: fullName,
    password: '',
    birth: ''
})

function verifyDate() {
    if (!userForm.value.birth) {
        return
    }
    let dateString = userForm.value.birth
    const thisYear = new Date().getFullYear()
    if (dateString.length == 8) {
        const verifyYearSliceString = dateString.slice(-2)
        const verifyYearSlice = Number(verifyYearSliceString)
        dateString = dateString.slice(0, -2)
        const thisYearSlice = thisYear - 2000

        if (verifyYearSlice >= thisYearSlice) {
            dateString += '19' + verifyYearSliceString
        } else {
            dateString += '20' + verifyYearSliceString
        }
        userForm.value.birth = dateString
    }
    if (dateString.length != 10) {
        return 'Data inválida'
    }

    const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/
    const match = dateString.match(dateRegex)
    if (!match) {
        return false
    }

    const day = parseInt(match[1], 10)
    const month = parseInt(match[2], 10)
    const year = parseInt(match[3], 10)

    if (year < 1900 || year >= thisYear) {
        return false
    }

    const date = new Date(year, month - 1, day)

    const is_date =
        date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day

    if (!is_date) return 'Data inválida'
}

function checkPasswordStrength() {
    const password = userForm.value.password || ''
    let strength = 0
    const conditions = [
        /[a-z]/, // lowercase letters
        /[A-Z]/, // uppercase letters
        /[0-9]/, // digits
        /[^A-Za-z0-9]/, // special characters
        /.{8,}/ // length greater than or equal to 8
    ]

    hasLowercase.value = /[a-z]/.test(password)
    hasUppercase.value = /[A-Z]/.test(password)
    hasNumber.value = /[0-9]/.test(password)
    hasSpecialChar.value = /[^A-Za-z0-9]/.test(password)

    conditions.forEach((regex) => {
        if (regex.test(password)) {
            strength++
        }
    })

    if (strength === 1) {
        strengthPassword.value = 'weak'
    } else if (strength === 2) {
        strengthPassword.value = 'moderate'
    } else if (strength === 3) {
        strengthPassword.value = 'good'
    } else if (strength === 4) {
        strengthPassword.value = 'strong'
    } else if (strength === 5) {
        strengthPassword.value = 'excellent'
    } else {
        strengthPassword.value = ''
    }
    passwordStrength.value
}

function RegisterUser() {
    registrando.value = true
    if (repeatPassword.value != userForm.value.password) {
        app.popup('Erro!', 'Senhas não conferem', 'warning', 2000)
        return
    }
    app.loading(true, 'Cadastrando...')
    app.api
        .post('/user/register/', userForm.value)
        .then(() => {
            app.popup(
                'Verifique seu e-mail!',
                'Usuário cadastrado com sucesso.<br><br> Verifique sua caixa de e-mail para confirmar',
                'warning',
                10000
            )
            router.push('/login')
        })
        .catch((error) => {
            app.popup('Erro!', app.resumeErrors(error), 'warning', 10000)
            registrando.value = false
        })
        .finally(() => {
            app.loading(false)
        })
}
</script>
<style>
.password-strength {
    height: 5px;
    background-color: #ddd;
    border-radius: 2px;
}

.password-strength-bar {
    height: 100%;
    transition: width 0.3s ease-in-out;
}

.password-strength-bar.weak {
    width: 20%;
    background-color: #e74c3c;
}

.password-strength-bar.moderate {
    width: 40%;
    background-color: #f39c12;
}

.password-strength-bar.good {
    width: 60%;
    background-color: #f1c40f;
}

.password-strength-bar.strong {
    width: 80%;
    background-color: #27ae60;
}

.password-strength-bar.excellent {
    width: 100%;
    background-color: #2ecc71;
}
</style>
