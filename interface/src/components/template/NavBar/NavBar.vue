<template>
        <nav class="navbar navbar-dark bg-dark ps-2 py-1 border-bottom border-secondary">
            <div class="row align-items-center w-100">
                <div class="col-12  d-flex align-items-center justify-content-center ms-2 py-3 border-bottom border-secondary">
                    <img src="/img/meuslares-logo.png"
                        alt="logo" class="square-image" @click="homepage">
                </div>
                <div class="col-8 text-white">
                    <div v-if="!email">
                        <div class="row text-center">
                            <div class="col-12 mb-0">
                                <span class="fw-bold">BEM VINDO</span>
                            </div>
                        </div>
                    </div>
                    <div v-else-if="email" class="row text-center">
                        <div class="col-12 mb-0">
                            <span class="fw-bold">{{ role }}</span>
                        </div>
                        <div class="col-12">
                            <span class="text-white">{{ email }}</span>
                        </div>
                    </div>
                </div>
                <div class="col-2 d-flex justify-content-end my-2">
                    <button class="navbar-toggler py-2 px-3" type="button" @click="notificationCollapse?.toggle()">
                        <i class="bi bi-bell"></i>
                    </button>
                </div>
                <div class="col-2 d-flex justify-content-start">
                    <button class="navbar-toggler py-2 px-3" type="button" @click="navCollapse?.toggle()">
                        <i class="bi bi-list"></i>
                    </button>
                </div>
            </div>
        </nav>
        <div id="main-nav" ref="mainNav">
        <div class="collapse bg-dark" id="navbarCollapse">
            <div class="pt-3">
                <a class="text-white text-decoration-none" @click="homepage">
                    <div class="d-flex mb-2 w-100 justify-content-center align-items-center">
                        <span>Página inicial</span>
                    </div>
                </a>
            </div>
            <div v-if="!email" class="pb-1">
                <router-link class="text-white text-decoration-none" to="/usuario/cadastro" @click="hide">
                    <div class="d-flex mb-2 w-100 justify-content-center align-items-center">
                        <span>Cadastre-se</span>
                    </div>
                </router-link>
                <router-link class="text-white text-decoration-none" to="/login" @click="hide">
                    <div class="d-flex mb-2 w-100 justify-content-center align-items-center">
                        <span>Entrar</span>
                    </div>
                </router-link>
            </div>
            <div v-else class="pb-1">
                <router-link class="text-white text-decoration-none" to="/usuario/papel" @click="hide">
                    <div class="d-flex mb-2 w-100 justify-content-center align-items-center">
                        <span>Mudar de perfil</span>
                    </div>
                </router-link>
                <a class="text-white text-decoration-none" to="/" @click="logout">
                    <div class="d-flex mb-2 w-100 justify-content-center align-items-center">
                        <span>Sair</span>
                    </div>
                </a>
            </div>
        </div>
        <div class="collapse bg-dark text-white" id="notificationCollapse">
            <div class="p-3">Notificações aqui</div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { userStore } from '@/modules/user/stores';
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import { api } from '@/http';
import { Collapse } from 'bootstrap';
import { roleMap } from '@/modules/user/interfaces';
import { useRouter } from 'vue-router';

const user = userStore();
const email = ref<string | null>(user.email);
const role = ref<string | null>(roleMap[user.role]);
const mainNav = ref<HTMLElement | null>(null);
const notificationCollapse = ref<Collapse | null>(null);
const navCollapse = ref<Collapse | null>(null);

const router = useRouter()


watch(
    () => user.email,
    (newUsername) => {
        email.value = newUsername;
    }

);

watch(
    () => user.role,
    (newRole) => {
        role.value = roleMap[newRole];
    }

);


async function logout() {
    hide()
    await api.logout();
}

function homepage() {
    if (!user.email){
        router.push('/')
        return
    }
    switch (user.role) {
        case "owner":
            router.push('/proprietario')
            break
        case "tenant":
            router.push('/morador')
            break
        case "":
            router.push('/usuario/papel')
            break
    }
}
onMounted(() => {
    document.addEventListener('click', handleClickOutside);
    const notification = document.getElementById("notificationCollapse");
    const navbar = document.getElementById("navbarCollapse");

    if (notification && navbar) {
        notificationCollapse.value = new Collapse(notification, { toggle: false });
        navCollapse.value = new Collapse(navbar, { toggle: false });
    }
});

onBeforeUnmount(() => {
    document.removeEventListener('click', handleClickOutside);
});

function handleClickOutside(event: MouseEvent) {
    if (mainNav.value && !mainNav.value.contains(event.target as Node)) {
        hide()
    }
}

function hide() {
    navCollapse.value?.hide()
    notificationCollapse.value?.hide();
}

</script>

<style>
.square-image {
    width: 300px;
    height: 40px;
    object-fit: cover;
    border-radius: 10px;
    overflow: hidden;
}
</style>