<template>
    <form v-if="searchable" @submit.prevent="updateList()">
        <div class="input-group mb-3">
            <input
                v-model="searchQuery"
                type="text"
                placeholder="Pesquisar..."
                class="form-control"
                aria-label="Pesquisar"
            />
            <button class="btn btn-outline-secondary" type="submit" id="button-addon2">
                <i class="bi bi-search"></i>
            </button>
            <button @click="updateList(true)" type="button" class="btn btn-outline-secondary">
                <i class="bi bi-arrow-clockwise"></i>
            </button>
        </div>
    </form>
    <div>
        <div v-if="listData.length === 0" class="alert alert-info text-center">
            Nenhum disponível no momento.
        </div>
        <div v-else-if="loading" class="d-flex justify-content-center m-3">
            <div class="spinner-border text-secondary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else class="row">
            <div v-for="(item, i) in listData" :key="i" class="col-12 col-md-6 col-lg-4">
                <div class="card my-2 mx-1 p-0">
                    <router-link :to="item['redirect']" class="text-decoration-none text-dark">
                        <div class="row g-0" @click="redirect(item)">
                            <div v-if="props.img" class="col-5">
                                <img
                                    :src="
                                        item[props.img]
                                            ? item[props.img]
                                            : 'https://cdn-icons-png.flaticon.com/512/1066/1066153.png'
                                    "
                                    class="img-fluid rounded-start"
                                    alt="..."
                                />
                            </div>
                            <div class="col">
                                <div class="card-body">
                                    <div class="m-0 p-0">
                                        <h6 v-if="props.title">{{ item[props.title] }}</h6>
                                        <div class="card-span">
                                            <span v-for="(v, k) in headers">
                                                <small v-if="v !== null">
                                                    <br />
                                                    <strong v-if="v">
                                                        <div class="mb-1" />
                                                        {{ v }}
                                                    </strong>
                                                    <br v-if="v" />
                                                    <span
                                                        v-if="item[k] === false || item[k] === true"
                                                    >
                                                        {{ item[k] ? 'Sim' : 'Não' }}
                                                    </span>
                                                    <span v-else>
                                                        {{ item[k] }}
                                                    </span>
                                                </small>
                                            </span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </router-link>
                </div>
            </div>
            <div v-if="previousPage || nextPage" class="input-group d-flex justify-content-center">
                <button class="btn btn-secondary" @click="goPreviousPage" :disabled="!previousPage">
                    Anterior
                </button>
                <span class="input-group-text">{{ page }} de {{ Math.ceil(total / 24) }}</span>
                <button class="btn btn-secondary" @click="goNextPage" :disabled="!nextPage">
                    Próxima
                </button>
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
    start: boolean
    title?: string
    cashTime?: number
    headers?: { [key: string]: string | null }
    img?: string
    redirect?: string
    params?: string[]
    searchable?: boolean
}>()

const headers = ref(props.headers || inputsLabel)
const searchQuery = ref('')
const listData = ref<Item[]>([])
const previousPage = ref<string | null>(null)
const nextPage = ref<string | null>(null)
const page = ref<number>(1)
const total = ref<number>(0)
const loading = ref<boolean>(false)
const start = ref<boolean>(props.start)
let firstUpdate = false

watch(
    () => props.start,
    () => {
        if (firstUpdate) {
            updateList()
        }
    }
)

function goNextPage() {
    if (nextPage.value) {
        page.value++
        updateList()
    }
}

function goPreviousPage() {
    if (previousPage.value) {
        page.value--
        updateList()
    }
}

function redirect(item: Item) {
    let url = '/' + props.redirect
    props.params?.forEach((prop) => {
        url += '/' + item[prop]
    })
    url += '/'
    return url
}

onMounted(() => {
    if (start.value) updateList()
})

function updateList(force: boolean = false) {
    loading.value = true
    let query = ''

    if (props.url.includes('?')) {
        query = `&page=${page.value}`
    } else {
        query = `?page=${page.value}`
    }

    if (searchQuery.value) query += `&search=${searchQuery.value}`

    api.getListCashed<Item[]>(props.url + query, force, props.cashTime, props.url)
        .then(({ result, next, previous, count }) => {
            listData.value = result
            nextPage.value = next
            previousPage.value = previous
            total.value = count

            if (props.redirect) {
                listData.value.forEach((item, index) => {
                    listData.value[index].redirect = redirect(item)
                })
                processData(listData.value)
            }
        })
        .catch(() => {
            popup('Erro!', 'Falha ao listar', 'warning')
        })
        .finally(() => {
            loading.value = false
        })
}

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
</script>

<style scoped>
.card-span {
    font-size: 0.5rem;
    line-height: 1.25;
}
</style>
