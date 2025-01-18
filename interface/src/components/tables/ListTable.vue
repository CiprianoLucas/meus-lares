<template>
    <div v-if="listData.length === 0" class="alert alert-info text-center">
        Nenhum disponível no momento.
    </div>

    <div v-else>
        <form @submit.prevent="updateTable">
            <div class="input-group mb-3">
                <input v-model="searchQuery" type="text" placeholder="Pesquisar..." class="form-control"
                    aria-label="Pesquisar" />
                <button class="btn btn-outline-secondary" type="submit" id="button-addon2">
                    Pesquisar
                </button>
            </div>
        </form>
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th v-for="(v, k) in columns" :key="k">
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
        <div class="input-group">
            <button class="btn btn-secondary" @click="goPreviousPage" :disabled="!previousPage">
                Anterior
            </button>
            <span class="input-group-text">{{ total }} registro(s)</span>
            <button class="btn btn-secondary" @click="goNextPage" :disabled="!nextPage">
                Próxima
            </button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { api } from '@/http'
import { popup } from '../PopUps'

interface Item {
    [key: string]: any
}

const props = defineProps<{
    url: string
    headers?: { [key: string]: string | null }
    columnPath?: { [key: string]: string }
    paramPath?: { [key: string]: string }
    cashTime?: number
    hide?: (string | number)[]
}>()

const searchQuery = ref<string | null>(null)
const previousPage = ref<string | null>(null)
const nextPage = ref<string | null>(null)
const page = ref<number>(1)
const total = ref<number>(0)
const listData = ref<Item[]>([])
const columns = ref<{ [key: string]: string }>({})

function goNextPage() {
    if (nextPage.value) {
        page.value--
        updateTable()
    }
}

function goPreviousPage() {
    if (previousPage.value) {
        page.value++
        updateTable()
    }
}

function redirect(item: Item, key: string | number) {
    if (props.columnPath && props.paramPath) {
        const path = props.columnPath[key]
        let newPath = path
        Object.entries(props.paramPath).forEach(([k, v]) => {
            newPath = path.replace(new RegExp(k, 'g'), item[v]);
        });
        return (path == newPath) ? ("") : ("/" + newPath)
    }
    return ""
}

function celClass(item: Item, key: string | number){
    let celClass = "link-offset-2 link-underline link-underline-opacity-0"
    if (redirect(item, key)){
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
    updateTable()
})

function updateTable() {
    let query = `?page=${page.value}`
    if (searchQuery.value) query += `&search=${searchQuery.value}`

    api.getListCashed<Item[]>(props.url + query, true, props.cashTime)
        .then(({ result, next, previous, count }) => {
            listData.value = result
            nextPage.value = next
            previousPage.value = previous
            total.value = count
        })
        .catch(() => {
            popup('Erro!', 'Falha ao listar', 'warning')
        })
}
</script>

<style scoped></style>
