# Connect Innova

O Connect Innova é uma plataforma digital que apoia estudantes universitários na preparação e evolução de seus projetos acadêmicos. A solução oferece análise inicial estruturada dos trabalhos, identifica pontos fortes e melhorias e conecta os projetos a editais de fomento, aproximando-os de oportunidades reais.

---

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

```bash
cd backend 
pip install uv
uv sync && source .venv/bin/activate
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
