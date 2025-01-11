<template>
    <div v-if="listData.length === 0" class="alert alert-info text-center">
        Nenhum disponível no momento.
    </div>

    <div v-else>
        <form @submit.prevent="handleSearch">
            <div class="input-group mb-3">
                <input v-model="searchQuery" type="text" placeholder="Pesquisar..." class="form-control"
                    aria-label="Pesquisar" />
                <button class="btn btn-outline-secondary" type="submit" id="button-addon2">
                    Pesquisar
                </button>
            </div>
        </form>
        <div>
            <div v-for="(item, i) in listData" :key="i" class="card">
                <router-link :to="item['redirect']" class="text-decoration-none text-dark">
                    <div class="row g-0" @click="redirect(item)">
                        <div v-if="props.img" class="col-4 d-flex justify-content-center align-items-center">
                            <img :src="item[props.img] ? item[props.img] : 'https://cdn-icons-png.flaticon.com/512/1066/1066153.png'"
                                class="img-fluid rounded-start" alt="...">
                        </div>
                        <div class="col">
                            <div class="card-body">
                                <div v-for="(v, k) in headers">
                                    <h5 v-if="k == props.title">{{ item[k] }}</h5>
                                    <p class="mb-1" v-if="!props.hide?.includes(k)"><small><strong>{{ v
                                                }}:</strong><br>{{
                                                    item[k] }}</small></p>
                                </div>
                            </div>
                        </div>
                    </div>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, onMounted } from 'vue'
import { inputsLabel } from '../forms'
import { api } from '@/http'
import { popup } from '../PopUps'

interface Item {
    [key: string]: any
}

const props = defineProps<{
    url: string
    title?: string
    cashTime?: number
    headers?: { [key: string]: string }
    img?: string
    redirect?: string
    params?: string[]
    hide?: (string | number)[]
}>()

const headers = ref(props.headers || inputsLabel)
const searchQuery = ref('')
const listData = ref<Item[]>([])
const forceUpdate = ref<Item[]>([])

function redirect(item: Item) {
    let url = '/' + props.redirect
    props.params?.forEach(prop => {
        url += ("/" + item[prop])
    });
    url += "/"
    return url
}

onMounted(() => {
    api
        .getListCashed<Item[]>(props.url, false,)
        .then(({ result }) => {
            listData.value = result
            if (props.redirect) {
                listData.value.forEach((item, index) => {
                    listData.value[index].redirect = redirect(item)
                });
                props.hide?.push('redirect')
            }
        })
        .catch(() => {
            popup('Erro!', 'Falha ao listar', 'warning')
        })
})

function handleSearch() { }

const processData = (data: Item[]) => {
    const keys = Object.keys(headers.value)
    if (listData.value.length > 0) {
        keys.forEach((element) => {
            if (!listData.value[0]?.[element]) {
                delete headers.value[element]
            }
        })
    }
}

watch(
    () => listData.value,
    (newData) => {
        processData(newData)
    },
    { immediate: true }
)
</script>

<style scoped>
img {
    width: 100px;
    height: 100px;
}
</style>
