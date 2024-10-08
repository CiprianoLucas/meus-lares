# Centro de Gestão para Condomínios
Centro facilitador para condomínios, utilizando de diversas tecnologias para as mais diversas necessidades do mercado.

## Propósito
O objetivo deste projeto é facilitar o dia a dia dos residentes de um condomínio e dos responsáveis pela gestão, permitindo a criação e acompanhamento de chamados de manutenção e reclamação, integrações com sistemas públicos, interatividade com as informações disponibilizadas e demais funcionalidades. A aplicação busca agilizar a resolução de problemas, melhorar a organização interna e proporcionar maior transparência no gerenciamento das demandas dos residentes.

## Funcionalidades aplicadas
- Cadastro e Login de Usuários: Os usuários podem se registrar e fazer login para acessar o sistema.

- Criação de Chamados: Os residentes podem criar chamados de manutenção e reclamação.

- Acompanhamento de Chamados: Os usuários podem visualizar e acompanhar o status de seus chamados.

- Gestão de Chamados: Os gestores do condomínio podem gerenciar e responder aos chamados.

- Chat com Inteligência artificial para solicitar informações de dentro da aplicação.

- Integração com a CELESC para recebimento simplificado das faturas

## Tecnologias Utilizadas
- Backend:
    - **Django Rest Framework**
    - imap
    - boto3
    - gunicorn
    - poetry

- Frontend:
    - **Vue 3**
    - Bootstrap
    - Axios
    - Vite
    - Pinea
    - Typescript
    
- Infraestrutura:
    - **Docker**
    - **PostgreSQL**
    - cron
    - supervisor

## Instalação
### Pré-requisitos obrigatórios
- Docker ^25.0.3

### Pré-requisitos para desenvolvimento
- Docker ^25.0.3
- Node ^18
- Python ^3.12
- Poetry ^1.8.3

### Clonando o Repositório

```bash
git clone https://github.com/CiprianoLucas/meus-lares.git
cd meus-lares
```

## Configuração obrigatória
- Configure as variáveis de ambiente necessárias, como credenciais do banco de dados e chaves secretas, utilize os arquivos.exaple_env para criar um .env

- Certifique-se de que o backend e o frontend estejam apontando para os respectivos servidores e endpoints.

- Se você está usando Windows, provavelmente precisará ir ao arquivo /api/crontab e mudar de CRLF para LF

### Configurando o ambiente
Com docker em funcionamento, execute o comando para criar o container
```bash
docker compose up -d --build
```

### Como demonstrar
Após realizar a instalação e configuração. Acesse a aplicação em http://localhost:{INTERFACE_PORT} para utilizar o frontend e http://localhost:{API_PORT} para visualizar os endpoints do backend.

## Configuração desenvolvimento
**Efetue a configuração obrigatória**

O projeto é separado em duas aplicações, API (backend) e INTERFACE (frontend)

### Desenvolvimento Frontend
Recomendo utilizar o endpoint do docker para fazer as requisições para o backend em vez do repositório principal.

A partir do diretório raiz do projeto, acesse o diretório de frontend:
```bash
cd ./interface
```

Faça a instalação das dependências:
```bash
npm i
```

Faça rodar com visualização de modificações ativa:
```bash
npm run dev
```
Ao fazer esse comando ele retornará o endereço para visualizar a página. A tela será atualizada sempre que modificar o diretório

### Desenvolvimento Backend

A partir do diretório raiz do projeto, acesse o diretório de backend:
```bash
cd ./api
```

Inicialmente precisamos criar um ambiente virtual e carrega-lo, execute:

- _Windows_
```bash
python -m venv venv
venv ./venv/Scripts/activate
poetry install --with dev
```

- _Linux e Mac_
```bash
python -m venv venv
venv ./venv/bin/activate
poetry install --with dev
```

Para iniciar o servidor localmente execute:
```bash
python manage.py runserver
```
Ao fazer esse comando ele retornará o endereço para visualizar a página. A API será atualizada sempre que modificar o diretório

Se modificar algum model, será necessário efetuar as migrações, então execute:
```bash
python manage.py makemigrations
python manage.py migrate
```