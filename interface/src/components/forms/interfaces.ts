interface Options {
    value?: string | number
    active?: boolean
    label: string
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
}

export type { Options, Input }
