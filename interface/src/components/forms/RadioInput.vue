<template>
    <label v-if="label" :for="id" class="form-label"
        >{{ label }}
        <help-button
            v-if="helpTooltip || helpModal"
            :tooltip="helpTooltip"
            :modal="helpModal"
            :id="id"
    /></label>
    <div v-for="option in options" class="form-check">
        <input
            class="form-check-input"
            :value="option[optionValue]"
            type="radio"
            v-bind="$attrs"
            :name="`name-radio-${id}`"
            :id="`radio-${option[optionValue]}-${id}`"
            v-model="localValue"
        />
        <label class="form-check-label" :for="`radio-${option[optionValue]}-${id}`">
            {{ option[optionLabel] }}
        </label>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions } from 'vue'
import HelpButton from '../PopUps/HelpButton.vue'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    optionValue: string
    optionLabel: string
    options: { [key: string]: string | number }[]
    helpTooltip?: string
    helpModal?: string
    modelValue?: string | null | number
    label?: string
}>()

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
</script>
