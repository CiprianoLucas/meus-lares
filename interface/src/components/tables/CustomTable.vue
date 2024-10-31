<template>
    <div v-if="props.data.length === 0" class="alert alert-info text-center">
        Nenhum disponível no momento.
    </div>

    <div v-else>
        <input v-model="searchQuery" placeholder="Pesquisar..." class="form-control mb-3" />
        <div class="table-responsive">
            <table class="table table-striped">
                <thead>
                    <tr>
                        <th v-for="(v, k) in headers" :key="k" @click="sortBy(k as string)"
                            :class="getThClass(k as string)">
                            {{ v }}
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(item, i) in paginatedData" :key="i">
                        <td v-for="(v, k) in headers" :key="v" :class="getTdClass(k as string)">
                            {{ item[k] }}
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="row">
            <div class="col-3">
                <div class="input-group input-group-sm">
                    <span class="input-group-text">Itens por página:</span>
                    <select v-model="itemsPerPage" class="form-select" aria-label="Sizing example input"
                        aria-describedby="inputGroup-sizing-sm">
                        <option :value="20">20</option>
                        <option :value="50">50</option>
                        <option :value="100">100</option>
                    </select>
                </div>
            </div>
            <div class="col">
                <div class="input-group ">
                    <button class="btn btn-secondary" @click="previousPage"
                        :disabled="currentPage === 1">Anterior</button>
                    <span class="input-group-text">Página {{ currentPage }} de {{ totalPages }}</span>
                    <button class="btn btn-secondary" @click="nextPage"
                        :disabled="currentPage === totalPages">Próxima</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'
import { inputsLabel } from '../forms';

interface Item { [key: string]: any }

const props = defineProps<{
    data: Item[]
    headers?: { [key: string]: string }
}>()


const headers = ref(props.headers || inputsLabel)
const searchQuery = ref('')
const sortKey = ref<string | null>(null)
const sortOrder = ref(1)
const currentPage = ref(1)
const itemsPerPage = ref(20)

const filteredAndSortedData = computed(() => {
    let result = props.data
    if (searchQuery.value) {
        result = result.filter((item) =>
            Object.keys(headers.value).some((k) =>
                String(item[k])
                    .toLowerCase()
                    .includes(searchQuery.value.toLowerCase())
            )
        )
    }

    if (sortKey.value) {
        result = result.slice().sort((a: Item, b: Item) => {
            const aValue = a[sortKey.value as keyof Item].toString().toLowerCase();
            const bValue = b[sortKey.value as keyof Item].toString().toLowerCase();

            if (aValue < bValue) return sortOrder.value === 1 ? -1 : 1;
            if (aValue > bValue) return sortOrder.value === 1 ? 1 : -1;
            return 0;
        });
    }

    return result
});

const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredAndSortedData.value.slice(start, end);
});

const totalPages = computed(() =>
    Math.ceil(filteredAndSortedData.value.length / itemsPerPage.value)
);

const resetPage = () => {
    currentPage.value = 1;
};

const sortBy = (key: string) => {
    if (sortKey.value === key) {
        sortOrder.value = -sortOrder.value;
    } else {
        sortKey.value = key;
        sortOrder.value = 1;
    }
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
    }
};

const previousPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
    }
};

const getThClass = (key: string) => {
    let thClass = ""
    if (key ==="state"){
        thClass += "sticky-last-column "
    }
    if (sortKey.value === key) {
        thClass += sortOrder.value === 1 ? 'ascending' : 'descending';
    }
    return thClass;
};

const getTdClass = (key: string) => {
    let tdClass = ""
    if (key ==="state"){
        tdClass += "sticky-last-column"
    }
    return tdClass;
};

watch(searchQuery, resetPage);
</script>

<style scoped>
.table-responsive {
  overflow-x: auto;
}

.sticky-last-column {
  position: sticky;
  right: 0;
  z-index: 1;
}

.table th,
.table td {
    border: 1px solid #ddd;
}

th {
    cursor: pointer;
}

.table th.ascending::after {
    content: ' ▲';
}

.table th.descending::after {
    content: ' ▼';
}
</style>