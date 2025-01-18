type Role = "" | "tenant" | "owner";

interface User {
    id?: string
    nick?: string
    cpf?: string
    phone_number?: string
    full_name?: string
    password?: string
    email?: string
    birth?: string
}

const roleMap = {
    "": "",
    tenant: "Morador",
    owner: "Proprietário"
}

export type { User , Role}
export { roleMap }