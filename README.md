# 📝 Release Notes - Connect Innova

Versão alpha 1.0.0 - 01/12/2025

Bem vindo a versão 1.0.0 do Connect Innova!

O Connect Innova é uma plataforma digital que apoia estudantes universitários na preparação e evolução de seus projetos acadêmicos. A solução oferece análise inicial estruturada dos trabalhos, identifica pontos fortes e melhorias e conecta os projetos a editais de fomento, aproximando-os de oportunidades reais.

Esta é a versão traz a adição das principais features da versão alpha da plataforma, como a de cadastrar/editar/excluir projetos, dashboard contendo análises geradas por Inteligência Artificial dos projetos cadastrados. Temos o prazer de compartilhar e destrinchar o resultado inicial de meses de trabalho e dedicação a seguir:

## ⚙ Funcionalidades desenvolvidas nesta release:

- Fluxo de cadastro e login: Na plataforma você pode se cadastrar para armazenar suas próprias informações e seus projetos com segurança.
    - Caso sua senha seja perdida/esquecida, já é possível trocá-la através do botão de “esqueci minha senha”.
		

- Cadastro e Gerenciamento de projetos: Uma das principais funcionalidades da release. A partir dela você trará informações importantes sobre seu projeto que serão utilizadas para as análises feitas pela I.A
    - O cadastro não se perde ao atualizar a página.
    - Os campos do formulário possuem descrições com perguntas mais diretas para lhe levar a resposta do que preencher no devido campo.
    - Além do cadastro, também é possível excluir ou editar seus projetos, conforme você os altere ao alinhá-los às análises da I.A. através da tela de dashboard de análise. 

- Resumo e análise automatizada por I.A.: A principal funcionalidade da ferramenta. Após a submissão do seu projeto, a Inteligência Artificial produz uma análise do projeto submetido, categorizando-o em níveis e oferecendo sugestões de melhoria.
    - O modelo também produz um resumo do projeto para certificar-se de que entendeu tudo sobre o projeto, servindo como uma revisão para o usuário do que foi escrito.

- Dashboard de Análise: Para facilitar a visibilidade da análise feita pela LLM, disponibilizamos um dashboard com cards tematizados. Cada card possui:
    - Cor baseada nos níveis de 1 a 3, sendo vermelho para 1 (ruim), amarelo para 2 (médio) e verde para 3 (bom) 2- Médio, 3 - Bom) 
    - Conteúdo da sintetização feita pela I.A. no quesito específico, levando em conta o contexto do projeto. 
    - Uma sugestão de melhoria para cada ponto, descrita em azul.
  Além disso, nesta tela também é possível editar e excluir o projeto do respectivo dashboard

- Layout Responsivo: Pensando nos usuários mobile do sistema, nossa plataforma também se adapta aos diferentes tipos de dispositivos nos quais você possa estar acessando.

- Tela de seleção de projetos: Ao clicar na Home da plataforma, você encontrará a tela dos seus projetos, onde poderá selecionar projetos já inseridos para revisitar o dashboard, além da opção de cadastrar um novo projeto.


## 📝 Pré-requisitos

- Python
- Node.js
- MongoDB Atlas (já está criado)
- Docker e Docker Compose (opcional)
- **.env** na raiz do projeto com as variáveis preenchidas corretamente

---

## ⚡ Execução local

Clone o Repositório

```bash
git clone https://github.com/alanabclins/ConnectInnova.git
cd ConnectInnova/
```

### ⚙ Backend

1. Acesse a pasta e instale dependências:

linux e Mac:
```bash
cd backend 
pip install uv
uv sync && source .venv/bin/activate
```

ou no Windows:
```bash
cd backend 
pip install uv
uv sync && .venv\Scripts\activate
```

2. Rode a aplicação:

```bash
task run
```

- A API estará em: `http://localhost:8000`
- Superuser é criado automaticamente a partir do `.env`.

3. Testes:

```bash
task test
```

- Usa banco de teste `ConnectInnovaTest`, limpo antes/depois de cada execução
- Cobertura de testes em HTML: `coverage html`

4. Lint e formatação:

```bash
task lint
task format
```

---

### 🌐 Frontend

1. Acesse a pasta e instale dependências:

```bash
cd frontend
npm install
```

2. Rode a aplicação em desenvolvimento:

```bash
npm run dev
```

- O servidor estará disponível em `http://localhost:5173`
- Hot reload habilitado: alterações no código refletem automaticamente no navegador.

3. Build para produção:

```bash
npm run build
```

- Os arquivos finais são gerados na pasta `dist/`.

4. Lint e formatação:

```bash
npm run lint
npm run format
```

> **⚠ IMPORTANTE**: Para rodar o lint do codigo frontend, instalar o Pritier no VSCode - Pesqusia nas extensões: `esbenp.prettier-vscode`

---

## 🐋 Docker Compose

NA RAIZ DAS PASTAS

```bash
docker compose up --build
```

- A aplicação estará disponível em `http://localhost:8000`.
- Certifique-se de que o `.env` está presente com os dados corretos.

---

## 📂 Estrutura do projeto

```
.
├── backend
│   ├── app
│   │   ├── auth
│   │   │   ├── auth.py
│   │   │   └── __init__.py
│   │   ├── config
│   │   │   ├── config.py
│   │   │   ├── __init__.py
│   │   │   └── logging.py
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models
│   │   │   ├── __init__.py
│   │   │   └── users.py
│   │   ├── routers
│   │   │   ├── api.py
│   │   │   ├── __init__.py
│   │   │   ├── login.py
│   │   │   └── users.py
│   │   └── schemas
│   │       ├── __init__.py
│   │       ├── tokens.py
│   │       └── users.py
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── README.md
│   ├── tests
│   │   ├── conftest.py
│   │   ├── __init__.py
│   │   ├── routers
│   │   │   ├── __init__.py
│   │   │   ├── test_login.py
│   │   │   └── test_users.py
│   │   └── utils.py
│   └── uv.lock
├── docker-compose.yml
├── frontend
│   ├── Dockerfile
│   ├── Dockerfile.development
│   ├── eslint.config.js
│   ├── index.html
│   ├── nginx.conf
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   │   ├── beanie.svg
│   │   ├── docker.png
│   │   ├── farmd-1.png
│   │   ├── farmd-2.png
│   │   ├── fastapi-mark.svg
│   │   ├── fastapi.png
│   │   ├── hook-forms.svg
│   │   ├── mongodb.png
│   │   ├── mui.svg
│   │   ├── react-router-mark.svg
│   │   ├── react.svg
│   │   └── vite.svg
│   ├── README.md
│   ├── src
│   │   ├── axios.ts
│   │   ├── components
│   │   │   ├── LoginForm.test.tsx
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.test.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   ├── TopMenuBar.test.tsx
│   │   │   ├── TopMenuBar.tsx
│   │   │   ├── UserProfile.test.tsx
│   │   │   └── UserProfile.tsx
│   │   ├── contexts
│   │   │   ├── auth.tsx
│   │   │   └── snackbar.tsx
│   │   ├── error-page.tsx
│   │   ├── fallback.tsx
│   │   ├── main.tsx
│   │   ├── models
│   │   │   └── user.ts
│   │   ├── router.tsx
│   │   ├── routes
│   │   │   ├── home.tsx
│   │   │   ├── login.tsx
│   │   │   ├── profile.tsx
│   │   │   ├── register.tsx
│   │   │   ├── root.tsx
│   │   │   ├── sso.login.tsx
│   │   │   ├── users.test.tsx
│   │   │   └── users.tsx
│   │   ├── services
│   │   │   ├── auth.service.ts
│   │   │   └── user.service.ts
│   │   ├── setupTest.ts
│   │   ├── theme.tsx
│   │   └── vite-env.d.ts
│   ├── tsconfig.app.json
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   └── vite.config.ts
└── README.md
```

---
