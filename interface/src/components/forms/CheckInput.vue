<template>
    <div class="form-check">
        <input :id="id" class="form-check-input" type="checkbox" v-model="localValue" v-bind="$attrs" />
        <label v-if="label" :for="id" class="form-check-label">{{ label }}</label>
        <help-button v-if="helpTooltip || helpModal" :tooltip="helpTooltip" :modal="helpModal" :id="id"/>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions, onMounted } from 'vue'
import { Tooltip } from 'bootstrap'
import HelpButton from '../PopUps/HelpButton.vue';

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    modelValue?: boolean
    label?: string
    tooltip?: string
    helpTooltip?: string
    helpModal?: string
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

