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
    condominium?: string
    identifier?: string
    complement?: string
    tenant?: string
    tenant_name?: string
}

export type { Condominium, Apartment }
