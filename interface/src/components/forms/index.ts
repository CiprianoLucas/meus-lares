import { type Input } from './interfaces'

const inputsLabel: { [key: string]: string } = {
  name: 'Nome',
  number: 'Número',
  street: 'Logradouro',
  city: 'Cidade',
  state: 'Estado',
  email: 'Email',
  company: 'Empresa',
  unit_number: 'Unidade condumidora',
  resident: 'Morador',
  place: 'Local',
  title: 'Título',
  description: 'Descrição',
  type: 'Tipo',
  username: 'Nome de usuário',
  cpf: 'CPF',
  phone_number: 'Telefone',
  full_name: 'Nome completo',
  password: 'Senha'
}

const inputsProps: Input[] = [
  {
    reference: 'name',
    label: 'Nome',
    size: 'lg',
    type: 'textarea'
  },
  {
    reference: 'state',
    label: 'Estado',
    size: 'sm',
    type: 'select',
    options: []
  },
  {
    reference: 'city',
    label: 'Cidade',
    size: 'md',
    type: 'select',
    options: []
  },
  {
    reference: 'street',
    label: 'Logradouro',
    size: 'lg',
    type: 'text'
  },
  {
    reference: 'number',
    label: 'Número',
    size: 'sm',
    type: 'check',
  },
]

export { inputsLabel, inputsProps }
