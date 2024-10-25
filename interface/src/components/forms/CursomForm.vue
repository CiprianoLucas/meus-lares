<template>
    <div>
        <div class="row" v-for="input in props.inputs">
            <div :class="input.class">
                <div v-if="input.type == 'text' || input.type == 'password' || input.type == 'email'">
                    <label :for="`${input.reference}-input`">{{ input.label }}</label>
                    <input :type="input.type" :name="input.reference" :id="`${input.reference}-input`" v-model="props.form[input.reference]">
                </div>
                <div v-else-if="input.type == 'select'">
                    <label :for="`${input.reference}-input`">{{ input.label }}</label>
                    <select class="form-select" aria-label="Default select example">
                        <option selected>Open this select menu</option>
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

import { ref, computed, watch, onBeforeMount } from 'vue';

interface Options {
    value?: string
    active?: boolean
    label: string
}

interface Input {
    reference: string,
    label: string;
    options?: Options[]
    size?: "sm" | "md" | "lg" | "xl"
    class?: string
    type?: "text" | "password" | "email" | "textarea" | "select" | "multiselect" | "check" | "radio"
}

const props = defineProps<{
    inputs: Input[]
    form: { [key: string]: string }
}>();

const treatedInputs = ref<Input[]>(props.inputs);

onBeforeMount(() => {
    let inputClass = ""
    for (let i = 0; i < treatedInputs.value.length; i++) {
        let input = treatedInputs.value[i]
        if (input.size === "sm") {
            inputClass = "col-12 col-sm-6 col-md-4 col-lg-3"
        } else if (input.size === "md") {
            inputClass = "col-12 col-sm-6 col-lg-4"
        } else if (input.size === "lg") {
            inputClass = "col-12 col-lg-6"
        } else {
            inputClass = "col-12"
        }


    }
})
</script>
