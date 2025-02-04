<template>
    <button
        :data-bs-toggle="modal ? 'modal' : ''"
        :data-bs-target="'#helpModal-' + id"
        ref="tooltipButton"
        class="btn btn-outline-secondary rounded-circle m-0 p-0 ms-2"
    >
        <i class="bi bi-question"></i>
    </button>
    <div
        class="modal fade"
        :id="'helpModal-' + id"
        tabindex="-1"
        :aria-labelledby="'helpModalLabel-' + id"
        aria-hidden="true"
    >
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" :id="'helpModalLabel-' + id">Explicação</h1>
                    <button
                        type="button"
                        class="btn-close"
                        data-bs-dismiss="modal"
                        aria-label="Close"
                    ></button>
                </div>
                <div class="modal-body" v-html="modal" />
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                        Fechar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
import { Tooltip } from 'bootstrap'
import { onMounted, ref } from 'vue'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    tooltip?: string
    modal?: string
}>()

const tooltipButton = ref<HTMLElement>()
onMounted(() => {
    if (tooltipButton.value && props.tooltip) {
        new Tooltip(tooltipButton.value, {
            title: props.tooltip,
            placement: 'top',
            trigger: 'hover'
        })
    }
})
</script>
