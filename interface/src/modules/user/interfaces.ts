type Role = '' | 'tenant' | 'owner'

interface User {
    id?: string
    nick?: string
    cpf?: string
    phone_number?: string
    full_name?: string
    password?: string
    email?: string
    birth?: string
    profile_photo?: string
    self_photo?: string
    verified_status?: 'verified' | 'pending' | 'in_progress' | 'rejected'
}

const verifiedStatusMap = {
    verified: 'Verificado',
    pending: 'Pendente',
    in_progress: 'Em andamento',
    rejected: 'Rejeitado'
}

const roleMap = {
    '': '',
    tenant: 'Morador',
    owner: 'Proprietário'
}

export type { User, Role }
export { roleMap, verifiedStatusMap }
