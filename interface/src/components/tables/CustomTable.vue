<template>
    <div>
        <!-- Campo de Pesquisa -->
        <input v-model="searchQuery" placeholder="Pesquisar..." class="search-input" />

        <!-- Tabela -->
        <table class="custom-table">
            <thead>
                <tr>
                    <th v-for="(header, index) in headers" :key="index" @click="sortBy(header.key)"
                        :class="getSortClass(header.key)">
                        {{ header.label }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in paginatedData" :key="index">
                    <td v-for="(header, index) in headers" :key="index">
                        {{ item[header.key] }}
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- Controle de Paginação -->
        <div class="pagination-controls">
            <label>
                Itens por página:
                <select v-model="itemsPerPage" @change="resetPage">
                    <option :value="5">5</option>
                    <option :value="10">10</option>
                    <option :value="15">15</option>
                </select>
            </label>
            <button @click="previousPage" :disabled="currentPage === 1">Anterior</button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { ref, computed, watch } from 'vue'

// Definindo as tipagens das propriedades
interface Header {
    label: string
    key: string
}

interface DataItem {
    [key: string]: any
}

// Recebendo as propriedades com tipagem
const props = defineProps<{
    data: DataItem[]
    headers: Header[]
}>()

// Variáveis reativas
const searchQuery = ref('')
const sortKey = ref<string | null>(null)
const sortOrder = ref(1)
const currentPage = ref(1)
const itemsPerPage = ref(5)

// Computed para dados filtrados e ordenados
const filteredAndSortedData = computed(() => {
    let result = props.data

    // Filtragem
    if (searchQuery.value) {
        result = result.filter((item) =>
            props.headers.some((header) =>
                String(item[header.key])
                    .toLowerCase()
                    .includes(searchQuery.value.toLowerCase())
            )
        )
    }

    // Ordenação
    if (sortKey.value) {
        result = result.slice().sort((a, b) => {
            const aValue = a[sortKey.value as keyof DataItem]
            const bValue = b[sortKey.value as keyof DataItem]

            if (aValue < bValue) return sortOrder.value === 1 ? -1 : 1
            if (aValue > bValue) return sortOrder.value === 1 ? 1 : -1
            return 0
        })
    }

    return result
});

// Computed para dados paginados
const paginatedData = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value;
    const end = start + itemsPerPage.value;
    return filteredAndSortedData.value.slice(start, end);
});

// Total de páginas
const totalPages = computed(() =>
    Math.ceil(filteredAndSortedData.value.length / itemsPerPage.value)
);

// Função para resetar a página
const resetPage = () => {
    currentPage.value = 1;
};

// Função de ordenação ao clicar no cabeçalho
const sortBy = (key: string) => {
    if (sortKey.value === key) {
        sortOrder.value = -sortOrder.value; // Inverte a ordem se a coluna for a mesma
    } else {
        sortKey.value = key;
        sortOrder.value = 1;
    }
};

// Navegação entre páginas
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

// Classe para indicar ordenação na coluna
const getSortClass = (key: string) => {
    if (sortKey.value === key) {
        return sortOrder.value === 1 ? 'ascending' : 'descending';
    }
    return '';
};

// Observa mudanças no query de busca para resetar a página
watch(searchQuery, resetPage);
</script>

<style scoped>
.custom-table {
    width: 100%;
    border-collapse: collapse;
}

.custom-table th,
.custom-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    cursor: pointer;
}

.custom-table th.ascending::after {
    content: ' ▲';
}

.custom-table th.descending::after {
    content: ' ▼';
}

.search-input {
    margin-bottom: 10px;
    padding: 8px;
    width: 100%;
}

.pagination-controls {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: 10px;
}

.pagination-controls select {
    padding: 5px;
}

.pagination-controls button {
    padding: 5px 10px;
    cursor: pointer;
}
</style>