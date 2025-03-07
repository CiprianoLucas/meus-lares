import type { Apartment } from "../places/interfaces"
import type { User } from "../user/interfaces"

interface Tenant {
    apartment?: string
    apartment_details?: Apartment
    user?: string
    user_details?: User
    is_renter?: boolean
    is_responsible?: boolean
    is_first_contact?: boolean
    notes?: string
    contracts?: string
    is_active?: boolean
}
export type { Tenant }
