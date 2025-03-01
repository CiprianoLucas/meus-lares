<template>
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <div class="mb-3">
        <div class="input-group">
            <input
                v-bind="$attrs"
                v-model="localValue"
                :class="`form-control ${!valid ? 'border-danger' : ''}`"
                :id="id"
                @input="input"
                @change="change"
            />
            <span v-if="buttomLabel" class="input-group-text"
                ><button class="btn m-0 p-0" @click="buttomFunction?.apply" v-html="buttomLabel"
            /></span>
        </div>
        <div v-if="!valid && errorMessage" class="mt-1">
            <span class="text-danger">{{ errorMessage }}</span>
        </div>
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
    input?: Function
    mask?: string
    label?: string
    buttomLabel?: string
    buttomFunction?: Function
    validators?: Function[]
}>()

const localValue = ref(props.modelValue)
const label = ref(props.label || '')
const id = ref(props.id)
const valid = ref(true)
const errorMessage = ref(true)

const emit = defineEmits<{
    (event: 'update:modelValue', value?: string): void
}>()

function input() {
    verifyMask()
    props.input?.(localValue.value)
    emit('update:modelValue', localValue.value)
}

function change() {
    if (props.validators) {
        valid.value = true
        for (const validator of props.validators) {
            const error = validator(localValue)
            if (error) {
                valid.value = false
                errorMessage.value = error !== true ? error : ''
                break
            }
        }
    }
    emit('update:modelValue', localValue.value)
}

function verifyMask() {
    if (props.mask) {
        const maskedValue = applyMask(props.mask, localValue.value)
        localValue.value = maskedValue
        emit('update:modelValue', maskedValue)
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
