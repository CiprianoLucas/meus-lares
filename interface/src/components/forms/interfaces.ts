interface Options {
    label: string
    value: string | number
    active?: boolean
}

interface Input {
    reference: string
    label: string
    options?: Options[]
    size?: 'bit' | 'sm' | 'md' | 'lg' | 'xl'
    class?: string
    type?: 'text' | 'password' | 'email' | 'textarea' | 'select' | 'multiselect' | 'check' | 'radio'
    mask?: string
    placeholder?: string
    disabled?: boolean
}

export type { Options, Input }
