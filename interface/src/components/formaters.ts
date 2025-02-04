function formatPhoneNumber(phone: string = '') {
    phone = phone.replace(/\D/g, '')

    if (phone.length === 11) {
        return phone.replace(/^(\d{2})(\d{5})(\d{4})$/, '($1) $2-$3')
    } else if (phone.length === 10) {
        return phone.replace(/^(\d{2})(\d{4})(\d{4})$/, '($1) $2-$3')
    }
    return phone
}

function formatDate(date: string = '') {
    const [year, month, day] = date.split('-')
    return `${day}/${month}/${year}`
}

function formatCPF(cpf: string = '') {
    cpf = cpf.replace(/\D/g, '')
    return cpf.replace(/^(\d{3})(\d{3})(\d{3})(\d{2})$/, '$1.$2.$3-$4')
}

function objectToFormData(
    obj: Record<string, any>,
    formData = new FormData(),
    parentKey = ''
): FormData {
    Object.keys(obj).forEach((key) => {
        const value = obj[key]
        const formKey = parentKey ? `${parentKey}[${key}]` : key

        if (value instanceof File) {
            formData.append(formKey, value)
        } else if (Array.isArray(value)) {
            value.forEach((item, index) => {
                formData.append(`${formKey}[${index}]`, item)
            })
        } else if (typeof value === 'object' && value !== null) {
            objectToFormData(value, formData, formKey)
        } else {
            formData.append(formKey, String(value))
        }
    })

    return formData
}

export { formatPhoneNumber, formatDate, formatCPF, objectToFormData }
