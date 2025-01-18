<template>
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <div class="input-group mb-3">
        <input v-bind="$attrs" v-model="localValue" :class="`form-control ${!valid ? 'border-danger' : ''}`" :id="id"
        @input="input" @change="change"/>
        <span v-if="buttomLabel"class="input-group-text"><button class="btn m-0 p-0" @click="buttomFunction?.apply" v-html="buttomLabel"/></span>
    </div>
    <div v-if="!valid && errorMessage" class="mt-2">
        <span class="text-danger">{{ errorMessage }}</span>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions } from 'vue'
import applyMask from './mask'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    modelValue?: string
    mask?: string
    label?: string
    buttomLabel?: string
    buttomFunction?: Function
    validators?: Function[]
}>()

const localValue = ref(props.modelValue)
const label = ref(props.label || "")
const id = ref(props.id)
const valid = ref(true)
const errorMessage = ref(true)

const emit = defineEmits<{
    (event: 'update:value', value: string): void
}>()

function input() {
    verifyMask()
}

function change() {
    if (props.validators) {
        valid.value = true
        for (const validator of props.validators) {
            const error = validator()
            if (error) {
                valid.value = false
                errorMessage.value = error !== true ? error : ""
                break
            }
        }
    };
}

function verifyMask() {
    if (props.mask) {
        const maskedValue = applyMask(props.mask, localValue.value)
        localValue.value = maskedValue
        emit('update:value', maskedValue)
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