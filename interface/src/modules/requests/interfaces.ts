interface Request {
    id: string;
    place_name: string,
    title: string,
    description: string,
    type: 'R' | 'M' | 'O',
    status: 'P' | 'A' | 'C';
}

const typeMap = {
    'R': 'Reclamação',
    'M': 'Manutenção',
    'O': 'Outros'
};

const statusMap = {
    'P': 'Pendente',
    'A': 'Andamento',
    'C': 'Concluído'
};

export type { Request }
export { typeMap, statusMap }
