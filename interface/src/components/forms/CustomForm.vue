<template>
    <div>
        <div class="row">
            <div v-for="input in inputs" :class="input.class">
                <div
                    v-if="input.type == 'text' || input.type == 'password' || input.type == 'email'"
                >
                    <label :for="`${input.reference}-input`" class="form-label">{{
                        input.label
                    }}</label>
                    <input
                        :type="input.type"
                        :name="input.reference"
                        :id="`${input.reference}-input`"
                        v-model="props.form[input.reference]"
                        class="form-control"
                        @input="verifyMask(input.mask, input.reference)"
                    />
                </div>
                <div v-else-if="input.type == 'select'">
                    <label :for="`${input.reference}-input`" class="form-label">{{
                        input.label
                    }}</label>
                    <select
                        v-model="props.form[input.reference]"
                        class="form-select"
                        aria-label="Default select example"
                    >
                        <option :value="''">-----</option>
                        <option
                            v-for="option in input.options"
                            :key="option.value"
                            :value="option.value"
                        >
                            {{ option.label }}
                        </option>
                    </select>
                </div>
                <div v-else-if="input.type == 'multiselect'">
                    <label :for="`${input.reference}-input`" class="form-label">{{
                        input.label
                    }}</label>
                    <multiselect
                        v-model="props.form[input.reference]"
                        :options="input.options"
                        :multiple="true"
                        :close-on-select="false"
                        :clear-on-select="false"
                        :preserve-search="true"
                        placeholder="Pesquisar"
                        track-by="label"
                        label="label"
                        deselectLabel="Remover"
                        selectedLabel="Selecionado"
                        selectLabel="Selecionar"
                    >
                        <template #selection="{ values, search, isOpen }">
                            <span v-if="values.length" v-show="!isOpen">
                                {{ values.length }} selecionados
                            </span>
                        </template>
                        <template #option="props">
                            <span class="option_label">{{ props.option.label }}</span>
                        </template>
                    </multiselect>
                </div>
                <div v-else-if="input.type == 'check'">
                    <input
                        v-model="props.form[input.reference]"
                        class="form-check-input"
                        type="checkbox"
                        :id="`${input.reference}-input`"
                    />
                    <label :for="`${input.reference}-input`" class="form-check-label ms-2">{{
                        input.label
                    }}</label>
                </div>
                <div v-else-if="input.type == 'radio'">
                    <div v-for="option in input.options" :key="option.value" class="form-check">
                        <input
                            class="form-check-input"
                            :value="option.value"
                            type="radio"
                            :name="`name-radio-${input.reference}`"
                            :id="`radio-${option.value}-${input.reference}`"
                            v-model="props.form[input.reference]"
                        />
                        <label
                            class="form-check-label"
                            :for="`radio-${option.value}-${input.reference}`"
                        >
                            {{ option.label }}
                        </label>
                    </div>
                </div>
                <div v-else-if="input.type == 'textarea'">
                    <label :for="`${input.reference}-input`" class="form-label">{{
                        input.label
                    }}</label>
                    <textarea
                        v-model="props.form[input.reference]"
                        class="form-control"
                        aria-label="Default select example"
                    />
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>
import { ref, onBeforeMount, onBeforeUnmount, onMounted, watch } from 'vue'
import { inputsProps } from '.'
import Multiselect from 'vue-multiselect'
import type { Input } from './interfaces'
import applyMask from './mask'

const props = defineProps<{
    form: { [key: string]: string | number }
    inputs?: Input[]
}>()

function verifyMask(mask: string | undefined, reference: string | number) {
    if (mask) {
        props.form[reference] = applyMask(mask, String(props.form[reference]))
    }
}

const inputs = ref(props.inputs ? props.inputs : inputsProps)

onBeforeMount(() => {
    for (let i = 0; i < inputs.value.length; i++) {
        let input = inputs.value[i]
        if (!(input.reference in props.form)) {
            inputs.value = inputs.value.filter(
                (propInput) => propInput.reference != input.reference
            )
            i = -1
            continue
        }
        let inputClass = 'mb-3 '

        if (input.size === 'sm') {
            inputClass += 'col-12 col-sm-6 col-md-4 col-lg-3'
        } else if (input.size === 'md') {
            inputClass += 'col-12 col-sm-6 col-lg-4'
        } else if (input.size === 'lg') {
            inputClass += 'col-12 col-lg-6'
        } else {
            inputClass += 'col-12'
        }
        inputs.value[i].class = inputClass
    }
})
</script>

<style scoped></style>
