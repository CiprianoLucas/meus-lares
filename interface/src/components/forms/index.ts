import type { Options, Input } from './interfaces'

const states = <Options[]>[
	{
		label: "Acre",
		value: "AC"
	},
	{
		label: "Alagoas",
		value: "AL"
	},
	{
		label: "Amapá",
		value: "AP"
	},
	{
		label: "Amazonas",
		value: "AM"
	},
	{
		label: "Bahia",
		value: "BA"
	},
	{
		label: "Ceará",
		value: "CE"
	},
	{
		label: "Distrito Federal",
		value: "DF"
	},
	{
		label: "Espírito Santo",
		value: "ES"
	},
	{
		label: "Goiás",
		value: "GO"
	},
	{
		label: "Maranhão",
		value: "MA"
	},
	{
		label: "Mato Grosso",
		value: "MT"
	},
	{
		label: "Mato Grosso do Sul",
		value: "MS"
	},
	{
		label: "Minas Gerais",
		value: "MG"
	},
	{
		label: "Pará",
		value: "PA"
	},
	{
		label: "Paraíba",
		value: "PB"
	},
	{
		label: "Paraná",
		value: "PR"
	},
	{
		label: "Pernambuco",
		value: "PE"
	},
	{
		label: "Piauí",
		value: "PI"
	},
	{
		label: "Rio de Janeiro",
		value: "RJ"
	},
	{
		label: "Rio Grande do Norte",
		value: "RN"
	},
	{
		label: "Rio Grande do Sul",
		value: "RS"
	},
	{
		label: "Rondônia",
		value: "RO"
	},
	{
		label: "Roraima",
		value: "RR"
	},
	{
		label: "Santa Catarina",
		value: "SC"
	},
	{
		label: "São Paulo",
		value: "SP"
	},
	{
		label: "Sergipe",
		value: "SE"
	},
	{
		label: "Tocantins",
		value: "TO"
	}
]

const inputsLabel: { [key: string]: string } = {
  name: 'Nome',
  number: 'Número',
  street: 'Logradouro',
  city_name: 'Cidade',
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
  password: 'Senha',
  error: 'Erro'
}

const inputsProps = <Input[]>([
	{
		reference: 'name',
		label: 'Nome',
		size: 'lg',
		type: 'text'
	},
	{
		reference: 'cep',
		label: 'Cep',
		size: 'sm',
		type: 'text',
		mask: '#####-###'
	},
	{
		reference: 'state',
		label: 'Estado',
		size: 'sm',
		type: 'select',
		options: states
	},
	{
		reference: 'city',
		label: 'Cidade',
		size: 'lg',
		type: 'select',
		options: []
	},
	{
		reference: 'neighborhood',
		label: 'Bairro',
		size: 'lg',
		type: 'text',
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
		type: 'text',
		mask: '########'
	},
	{
		reference: 'complement',
		label: 'Complemento',
		size: 'sm',
		type: 'text',
	},
])



export { inputsLabel, inputsProps, states }
