<template>
    <div>
        <form v-if="searchable" @submit.prevent="updateTable()">
            <div class="input-group mb-3">
                <input v-model="searchQuery" type="text" placeholder="Pesquisar..." class="form-control"
                    aria-label="Pesquisar" />
                <button class="btn btn-outline-secondary" type="submit" id="button-addon2">
                    <i class="bi bi-search"></i>
                </button>
                <button @click="updateTable(true)" type="button" class="btn btn-outline-secondary">
                    <i class="bi bi-arrow-clockwise"></i>
                </button>
            </div>
        </form>
        <div v-if="listData.length === 0" class="alert alert-light text-center">
            Nenhum registro encontrado.
        </div>
        <div v-else-if="loading" class="d-flex justify-content-center m-3">
            <div class="spinner-border text-secondary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
        <div v-else class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th v-for="(v, k) in columns" :key="k" @click="sort(k)">
                            {{ v }}
                        </th scope="col">
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, i) in listData" :key="i" scope="col">
                        <td v-for="(v, k) in columns" :key="v">
                            <router-link :to="redirect(item, k)" v-html="item[k]"
                                :class="celClass(item, k)"></router-link>
                        </td>
                    </tr>
                </tbody>
            </table>
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
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '@/http'
import { popup } from '../PopUps'

interface Item {
    [key: string]: any
}

const props = defineProps<{
    url: string
    start: boolean
    headers?: { [key: string]: string | null }
    columnPath?: { [key: string]: string }
    paramPath?: { [key: string]: string }
    cashTime?: number
    searchable?: boolean
}>()

const searchQuery = ref<string | null>(null)
const previousPage = ref<string | null>(null)
const nextPage = ref<string | null>(null)
const page = ref<number>(1)
const total = ref<number>(0)
const listData = ref<Item[]>([])
const columns = ref<{ [key: string]: string }>({})
const sortBy = ref<string | null>(null)
const sortAsc = ref<boolean>(true)
const loading = ref<boolean>(false)
const start = ref<boolean>(props.start === undefined ? true : props.start)
let firstUpdate = true

watch(
    () => props.start,
    () => {
        if (firstUpdate) {
            firstUpdate = false
            updateTable()
        }
    }
)

function sort(column: string | number) {
    if (sortBy.value == column) {
        sortAsc.value = !sortAsc.value
    } else {
        sortAsc.value = true
    }
    sortBy.value = String(column)
    updateTable()
}

function goNextPage() {
    if (nextPage.value) {
        page.value++
        updateTable()
    }
}

function goPreviousPage() {
    if (previousPage.value) {
        page.value--
        updateTable()
    }
}

function redirect(item: Item, key: string | number) {
    if (props.columnPath && props.paramPath) {
        const path = props.columnPath[key]
        if(path){
            let newPath = path
            Object.entries(props.paramPath).forEach(([k, v]) => {
                if (item[v]) {
                    newPath = newPath.replace(new RegExp(k, 'g'), item[v]);
                }
            });
            return (path == newPath) ? ("") : ("/" + newPath)
        }
    }
    return ""
}

function celClass(item: Item, key: string | number) {
    let celClass = "link-offset-2 link-underline link-underline-opacity-0"
    if (redirect(item, key)) {
        return celClass
    }
    return "text-dark " + celClass
}

onMounted(() => {
    if (props.headers) {
        columns.value = Object.fromEntries(
            Object.entries(props.headers).filter(([key, value]) => value !== null)
        ) as { [key: string]: string }
    }
    if (start.value) updateTable()
})

function updateTable(force: boolean = false) {
    loading.value = true
    let query = ""

    if (props.url.includes('?')) {
        query = `&page=${page.value}`
    } else {
        query = `?page=${page.value}`
    }

    if (searchQuery.value) query += `&search=${searchQuery.value}`

    if (sortBy.value) query += `&sort_by=${sortBy.value}&sort_asc=${sortAsc.value}`

    api.getListCashed<Item[]>(props.url + query, force, props.cashTime, props.url)
        .then(({ result, next, previous, count }) => {
            listData.value = flattenArray(result)
            nextPage.value = next
            previousPage.value = previous
            total.value = count
        })
        .catch(() => {
            popup('Erro!', 'Falha ao listar', 'warning')
        })
        .finally(() => {
            loading.value = false
        })
}

function flattenObject<T extends Record<string, any>>(obj: T, prefix = ''): Record<string, any> {
    return Object.keys(obj).reduce((acc, key) => {
        const newKey = prefix ? `${prefix}__${key}` : key;
        const value = obj[key];

        if (typeof value === 'object' && value !== null) {
            Object.assign(acc, flattenObject(value, newKey));
        } else {
            acc[newKey] = value;
        }
        return acc;
    }, {} as Record<string, any>);
}

function flattenArray<T extends Record<string, any>>(arr: T[]): Record<string, any>[] {
    return arr.map(item => flattenObject(item));
}
</script>

<style scoped></style>
