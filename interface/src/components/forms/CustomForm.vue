<template>
    <div>
        <div class="row">
            <div v-for="input in inputs" :class="input.class">
                <div v-if="input.type == 'text' || input.type == 'password' || input.type == 'email'">
                    <label :for="`${input.reference}-input`" class="form-label">{{ input.label }}</label>
                    <input :type="input.type" :name="input.reference" :id="`${input.reference}-input`"
                        v-model="props.form[input.reference]" class="form-control"
                        @input="verifyMask(input.mask, input.reference)">
                </div>
                <div v-else-if="input.type == 'select'">
                    <label :for="`${input.reference}-input`" class="form-label">{{ input.label }}</label>
                    <select v-model="props.form[input.reference]" class="form-select"
                        aria-label="Default select example">
                        <option selected>-----</option>
                        <option value="1">One</option>
                        <option value="2">Two</option>
                        <option value="3">Three</option>
                    </select>
                </div>
            </div>
        </div>
    </div>
</template>
<script lang="ts" setup>

import { ref, onBeforeMount } from 'vue';
import { inputsProps } from '.';
import type { Input } from './interfaces';
import applyMask from './mask';

const props = defineProps<{
    form: { [key: string]: string }
    inputs?: Input[]
}>();

function verifyMask(mask: string | undefined, reference: string) {
    if (mask) {
        props.form[reference] = applyMask(mask, props.form[reference])
    }
}

const inputs = ref(props.inputs ? props.inputs : inputsProps)

onBeforeMount(() => {
    let inputClass = ""
    for (let i = 0; i < inputs.value.length; i++) {
        let input = inputs.value[i]
        if (!(input.reference in props.form)) {
            inputs.value = inputs.value.filter(propInput => propInput.reference != input.reference)
            i =- 1
            continue
        }

        if (input.size === "sm") {
            inputClass = "col-12 col-sm-6 col-md-4 col-lg-3"
        } else if (input.size === "md") {
            inputClass = "col-12 col-sm-6 col-lg-4"
        } else if (input.size === "lg") {
            inputClass = "col-12 col-lg-6"
        } else {
            inputClass = "col-12"
        }
        inputs.value[i].class = inputClass


    }
})
</script>
