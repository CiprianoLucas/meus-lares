<template>
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <div v-for="option in options" class="form-check">
        <input class="form-check-input" @change="change" :value="option[optionValue]" type="radio" v-bind="$attrs"
            :name="`name-radio-${id}`" :id="`radio-${option[optionValue]}-${id}`" v-model="localValue" />
        <label class="form-check-label" :for="`radio-${option[optionValue]}-${id}`">
            {{ option[optionLabel] }}
        </label>
    </div>
    <div v-if="!valid && errorMessage" class="mt-2">
        <span class="text-danger">{{ errorMessage }}</span>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions } from 'vue'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    optionValue: string
    optionLabel: string
    options: { [key: string]: string | number }[]
    modelValue?: string | null | number
    label?: string
    validators?: Function[]
}>()

const localValue = ref(props.modelValue)
const label = ref(props.label || '')
const id = ref(props.id)
const valid = ref(true)
const errorMessage = ref(true)

const emit = defineEmits<{
    (event: 'update:value', value: string): void
}>()

function change() {
    if (props.validators) {
        valid.value = true
        for (const validator of props.validators) {
            const error = validator()
            if (error) {
                valid.value = false
                errorMessage.value = error !== true ? error : ''
                break
            }
        }
    }
}

watch(
    () => props.modelValue,
    (newValue) => {
        if (newValue !== localValue.value) {
            localValue.value = newValue
        }
    }
)
</script>
