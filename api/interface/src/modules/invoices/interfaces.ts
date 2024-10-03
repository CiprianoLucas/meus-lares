interface InvoiceRelation {
    id: string;
    company: 'CELESC',
    unit_number: string,
    resident: string,
    resident_name: string,
    place: string,
    place_name: string,
}

interface Invoice {
    id: string,
    value: number,
    company: string,
    ticket_number: string
}

const companyMap = {
    'CELESC': 'CELESC'
};

export {type InvoiceRelation,type Invoice, companyMap}
