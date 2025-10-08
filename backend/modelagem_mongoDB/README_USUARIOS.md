# Coleção Usuarios - MongoDB

## 📋 Descrição

Coleção responsável por armazenar os dados dos usuários do sistema ConnectInnova.

---

## 🗂️ Estrutura do Documento

### Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `nome` | string | Nome completo do usuário |
| `email` | string | Email único do usuário (validado por regex) |
| `senha_hash` | string | Hash da senha (bcrypt/argon2) |
| `data_criacao` | date | Data de criação do registro |

### Campos Opcionais

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `data_atualizacao` | date \| null | Data da última atualização do registro |
| `is_active` | boolean | Status ativo/inativo do usuário (padrão: true) |
| `provider` | string \| null | Provedor de autenticação (local, google, github) |
| `picture` | string \| null | URL da foto de perfil |

---

## 🔒 Validações

### Schema JSON

A coleção utiliza `$jsonSchema` para validação dos documentos:

- **Campos obrigatórios**: `nome`, `email`, `senha_hash`, `data_criacao`
- **Validação de email**: Padrão regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Tipos estritos**: Date para datas, Boolean para flags, String para textos

### Índices

1. **email_1** (único): Garante unicidade do email no sistema
2. **data_criacao_1**: Otimiza consultas ordenadas por data

---

## 📝 Exemplos de Uso

### Inserir novo usuário

```python
from datetime import datetime
from funcoes_mongoDB.db_connection import Usuarios_collection

novo_usuario = {
    "nome": "Maria Silva",
    "email": "maria@example.com",
    "senha_hash": "$2b$12$KIXxAbC123HashExemplo",
    "data_criacao": datetime.utcnow(),
    "is_active": True,
    "provider": "local",
    "picture": None
}

result = Usuarios_collection.insert_one(novo_usuario)
print(f"Usuário criado com ID: {result.inserted_id}")
```

### Buscar usuário por email

```python
from funcoes_mongoDB.db_connection import Usuarios_collection

usuario = Usuarios_collection.find_one({"email": "maria@example.com"})
if usuario:
    print(f"Nome: {usuario['nome']}")
    print(f"Ativo: {usuario.get('is_active', True)}")
```

### Atualizar usuário

```python
from datetime import datetime
from funcoes_mongoDB.db_connection import Usuarios_collection

Usuarios_collection.update_one(
    {"email": "maria@example.com"},
    {
        "$set": {
            "nome": "Maria Silva Santos",
            "data_atualizacao": datetime.utcnow()
        }
    }
)
```

### Soft Delete (desativar usuário)

```python
from datetime import datetime
from funcoes_mongoDB.db_connection import Usuarios_collection

Usuarios_collection.update_one(
    {"email": "maria@example.com"},
    {
        "$set": {
            "is_active": False,
            "data_atualizacao": datetime.utcnow()
        }
    }
)
```

### Listar apenas usuários ativos

```python
from funcoes_mongoDB.db_connection import Usuarios_collection

usuarios_ativos = Usuarios_collection.find({"is_active": True})
for usuario in usuarios_ativos:
    print(f"{usuario['nome']} - {usuario['email']}")
```

---

## 🧪 Testes

### Executar criação da coleção

```bash
cd backend
uv run python -m modelagem_mongoDB.colecoes_mongoDB
```

### Executar testes de validação

```bash
cd backend
uv run python -m modelagem_mongoDB.test_usuarios_collection
```

### Resultado esperado

```
✅ Testes Aprovados: 9
❌ Testes Falhados: 0
📈 Taxa de Sucesso: 100.0%
```

---

## 🔗 Integração

### Importar a coleção

```python
from funcoes_mongoDB.db_connection import Usuarios_collection

# Agora você pode usar Usuarios_collection em seus scripts
```

---

## ⚠️ Observações Importantes

1. **Email único**: O sistema não permite dois usuários com o mesmo email
2. **Senha**: Sempre armazene apenas o hash da senha, nunca a senha em texto plano
3. **Soft Delete**: Use o campo `is_active` para desativar usuários ao invés de deletar
4. **Timestamps**: Use `datetime.utcnow()` para consistência de timezone (ou `datetime.now(datetime.UTC)` no Python 3.12+)

---

## 📊 Status da Implementação

- ✅ Schema de validação criado
- ✅ Índices configurados
- ✅ Testes de validação passando
- ✅ Integração com `db_connection.py`
- ✅ Documentação completa

---

## 🔄 Próximos Passos Sugeridos

1. Criar funções CRUD em `funcoes_mongoDB/crud_usuarios.py`
2. Implementar endpoints REST na API FastAPI
3. Adicionar testes de integração
4. Implementar autenticação JWT
5. Criar relação com a coleção `Students` (se aplicável)

---

**Criado em**: 08/10/2025  
**Branch**: SCRUM-47  
**Task**: [Banco de Dados] Criar coleção usuarios

