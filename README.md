# Centro de Chamados para Condomínios
A aplicação tem como objetivo criar um centro de chamados de manutenção e reclamação para condomínios, utilizando Django Rest Framework para o backend e Vue 3 para o frontend.

## Propósito
O objetivo deste projeto é facilitar a comunicação entre os residentes de um condomínio e os responsáveis pela gestão, permitindo a criação e acompanhamento de chamados de manutenção e reclamação. A aplicação busca agilizar a resolução de problemas, melhorar a organização interna e proporcionar maior transparência no gerenciamento das demandas dos residentes.

## Funcionalidades
- Cadastro e Login de Usuários: Os usuários podem se registrar e fazer login para acessar o sistema.
- Criação de Chamados: Os residentes podem criar chamados de manutenção e reclamação.
- Acompanhamento de Chamados: Os usuários podem visualizar e acompanhar o status de seus chamados.
- Gestão de Chamados: Os gestores do condomínio podem gerenciar e responder aos chamados.
## Tecnologias Utilizadas
- Backend:
    - Django Rest Framework
- Frontend:
    - Vue 3
    - Bootstrap
    - Axios

## Instalação
### Pré-requisitos
- Python 3.8+
- Node.js 17+

### Clonando o Repositório

```bash
git clone https://github.com/CiprianoLucas/meus-lares.git
cd meus_lares
```

### Backend
1. Crie e ative um ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Para Linux/macOS
venv\Scripts\activate  # Para Windows
```

2. Instale as dependências do backend:
```
pip install -r requirements.txt
```
3. Crie o arquivo *".env"* com base no *".env.example"*

4. Execute as migrações:
```bash
python manage.py migrate
```

5. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

### Frontend

1. Navegue até a pasta do frontend:
```
cd _interface
```

2. Instale as dependências:
```
npm install
```

3. Inicie o servidor de desenvolvimento:

```
npm run dev
```

## Configuração
- Configure as variáveis de ambiente necessárias, como credenciais do banco de dados e chaves secretas.

- Certifique-se de que o backend e o frontend estejam apontando para os respectivos servidores e endpoints.

## Como Executar
Após realizar a instalação e configuração, execute o servidor backend e frontend como descrito acima. Acesse a aplicação em http://localhost:5173 para utilizar o frontend e http://localhost:8000/admin para gerenciar o backend.

#### Licença
Este projeto é licenciado sob a Creative Commons Attribution-NonCommercial (CC BY-NC).

