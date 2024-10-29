interface Options {
    value?: string
    active?: boolean
    label: string
}

interface Input {
    reference: string
    label: string
    options?: Options[]
    size?: "sm" | "md" | "lg" | "xl"
    class?: string
    type?: "text" | "password" | "email" | "textarea" | "select" | "multiselect" | "check" | "radio"
    mask?: string
}

export type {Options, Input}