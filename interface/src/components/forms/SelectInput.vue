<template>
    <label v-if="label" :for="id" class="form-label">{{ label }}</label>
    <div class="input-group mb-3">
        <multiselect
            v-model="localValue"
            :options="options"
            placeholder="Pesquisar"
            :track-by="optionLabel"
            :label="optionLabel"
            :preserve-search="true"
            :show-labels="false"
            :allow-empty="false"
            v-bind="$attrs"
        >
        </multiselect>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, defineProps, defineEmits, defineOptions } from 'vue'
import Multiselect from 'vue-multiselect'

defineOptions({
    inheritAttrs: false
})
const props = defineProps<{
    id: string
    optionLabel: string
    options: { [key: string]: string | number | boolean }[]
    modelValue?: string | null | number | object
    label?: string
    buttomLabel?: string
    buttomFunction?: Function
    validators?: Function[]
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
<style>
.multiselect__option--highlight {
    background: #6c757d;
}

.multiselect__option--highlight::after {
    background: #6c757d;
}

.multiselect__spinner::before,
.multiselect__spinner::after {
    border-color: #6c757d transparent transparent;
}
.multiselect__tag {
    background: #6c757d;
}

.multiselect__option--selected.multiselect__option--highlight {
    background: #6c757d;
}

.multiselect__option--selected.multiselect__option--highlight::after {
    background: #6c757d;
}

.multiselect__option--group-selected.multiselect__option--highlight {
    background: #6c757d;
}

.multiselect__option--group-selected.multiselect__option--highlight::after {
    background: #6c757d;
}
</style>
