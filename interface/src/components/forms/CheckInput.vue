<template>
    <div class="form-check">
        <input :id="id" class="form-check-input" type="checkbox" v-model="localValue" v-bind="$attrs" />
        <label v-if="label" :for="id" class="form-check-label">{{ label }}</label>
        <button v-if="tooltip" ref="tooltipButton" class="btn btn-outline-secondary rounded-circle m-0 p-0 ms-2">
        <i class="bi bi-question"></i></button>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions, onMounted } from 'vue'
import { Tooltip } from 'bootstrap'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    modelValue?: boolean
    label?: string
    tooltip?: string
}>()


const tooltipButton = ref<HTMLElement | null>(null)
const localValue = ref(props.modelValue)
const label = ref(props.label || '')
const id = ref(props.id)

const emit = defineEmits<{
    (event: 'update:value', value: string): void
}>()

watch(
    () => props.modelValue,
    (newValue) => {
        if (newValue !== localValue.value) {
            localValue.value = newValue
        }
    }
)

onMounted(() => {
    if (tooltipButton.value) {
        new Tooltip(tooltipButton.value, {
            title: props.tooltip,
            placement: "top",
            trigger: "hover",
        })
    }
})
</script>

