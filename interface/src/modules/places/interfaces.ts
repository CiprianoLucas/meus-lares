interface Condominium {
    id?: string
    name?: string
    complement?: string
    neighborhood?: string
    cep?: string
    street?: string
    number?: string
    city?: number
    city_name?: string
    state?: string
    profile_photo?: string
}

interface Apartment {
    id?: string
    condominium?: string
    identifier?: string
    complement?: string
    tenant?: string
    tenant_name?: string
    is_active?: boolean
}

interface Park {
    id?: string
    condominium?: string
    identifier?: string
    complement?: string
    apartment?: string
    apartment_identifier?: string
}

interface SharedPlace {
    id?: string
    condominium?: string
    identifier?: string
    complement?: string
    capacity?: number
    is_reserveable?: boolean
    clean_time?: number
}

export type { Condominium, Apartment, Park, SharedPlace }
