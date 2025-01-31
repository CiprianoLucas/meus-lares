<template>
    <div :class="class">
    <label v-if="!hideInput" for="formFile" class="form-label">{{label}}</label>
    <button v-else @click="triggerFileInput" :class="classButtom?classButtom:'btn btn-secondary py-0 my-1'">
        <small>{{ label }}</small>
    </button>
    <input ref="fileInputRef" :style="hideInput ? 'display: none' : ''" class="form-control" type="file" id="formFile" 
        @change="fileChange">
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions } from 'vue'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    label: string
    modelValue: File | null
    runWhenChange?: Function
    hideInput?: boolean
    class?: string
    classButtom?: string
}>()

const fileInputRef = ref<HTMLInputElement | null>(null)
const localValue = ref(props.modelValue)

function triggerFileInput() {
    fileInputRef.value?.click()
}

async function fileChange(event: Event) {
    const target = event.target as HTMLInputElement
    const file = target.files?.[0] || null
    localValue.value = file

    emit("update:modelValue", file);

    props.runWhenChange?.apply
}

const emit = defineEmits<{
    (event: 'update:modelValue', value: File | null): void;
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
