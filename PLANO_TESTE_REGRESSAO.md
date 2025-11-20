# Plano de Teste de Regressão - ConnectInnova

## ⚠️ Status do Plano

**Este é um PLANO DE TESTES (documentação) - os testes ainda precisam ser implementados!**

- ✅ **Planejamento**: Completo (140 casos de teste documentados)
- ⏳ **Implementação**: Pendente (testes precisam ser escritos em código)
- ⏳ **Automação**: Pendente (será automático após implementação)

### Como Funcionará Após Implementação

Uma vez implementados em código (usando pytest), os testes serão:
- ✅ **Automáticos**: Executáveis via `pytest` ou `task test`
- ✅ **Repetíveis**: Podem ser executados quantas vezes necessário
- ✅ **Integráveis em CI/CD**: Podem rodar automaticamente em pipelines
- ✅ **Rápidos**: Execução completa em segundos/minutos

---

## 📋 Objetivo
Garantir que todas as funcionalidades críticas do sistema continuem funcionando corretamente após mudanças no código, verificando que não houve regressões em funcionalidades já implementadas e testadas.

## 🎯 Escopo
Este plano cobre os testes de regressão para:
- **Backend API** (FastAPI + MongoDB)
- **Autenticação e Autorização**
- **Gerenciamento de Usuários**
- **Gerenciamento de Projetos**
- **Análise de Projetos com IA (Gemini)**
- **Geração de Resumos com IA**
- **Validações de Dados**

---

## 📦 Estrutura de Testes

### 1. Autenticação e Autorização

#### 1.1 Login e Tokens
- [ ] **RT-001**: Login com credenciais válidas retorna token de acesso
- [ ] **RT-002**: Login com credenciais inválidas retorna 401
- [ ] **RT-003**: Token válido permite acesso a endpoints protegidos
- [ ] **RT-004**: Token inválido/expirado retorna 401
- [ ] **RT-005**: Endpoint `/login/test-token` valida token corretamente
- [ ] **RT-006**: Requisições sem token retornam 401

#### 1.2 Permissões e Autorização
- [ ] **RT-007**: Superuser pode acessar todos os endpoints
- [ ] **RT-008**: Usuário normal não pode acessar endpoints de superuser
- [ ] **RT-009**: Usuário só pode acessar seus próprios projetos
- [ ] **RT-010**: Usuário não pode modificar projetos de outros usuários

---

### 2. Gerenciamento de Usuários

#### 2.1 Criação de Usuários
- [ ] **RT-011**: Criar usuário com dados válidos retorna 200
- [ ] **RT-012**: Criar usuário sem campo obrigatório (name) retorna 422
- [ ] **RT-013**: Criar usuário com email inválido retorna 422
- [ ] **RT-014**: Criar usuário com email duplicado retorna 400
- [ ] **RT-015**: Criar usuário com email em maiúsculas/minúsculas duplicado retorna 400
- [ ] **RT-016**: Senha é hasheada corretamente no banco
- [ ] **RT-017**: Usuário criado tem `is_superuser=False` por padrão
- [ ] **RT-018**: Usuário criado tem `is_active=True` por padrão

#### 2.2 Validação de Nome
- [ ] **RT-019**: Nome com caracteres especiais HTML (`<`, `>`) retorna 400
- [ ] **RT-020**: Nome com números retorna 400
- [ ] **RT-021**: Nome com caracteres inválidos retorna 400
- [ ] **RT-022**: Nome apenas com letras e espaços é aceito
- [ ] **RT-023**: Nome com acentos é aceito

#### 2.3 Perfil de Usuário
- [ ] **RT-024**: GET `/users/me` retorna dados do usuário autenticado
- [ ] **RT-025**: Superuser pode ver seu próprio perfil
- [ ] **RT-026**: Usuário normal pode ver seu próprio perfil
- [ ] **RT-027**: Perfil retorna `is_active` e `is_superuser` corretos

#### 2.4 Atualização de Usuário
- [ ] **RT-028**: Usuário pode atualizar seu próprio perfil
- [ ] **RT-029**: Atualização de email para email único é permitida
- [ ] **RT-030**: Atualização de email para email existente retorna 400
- [ ] **RT-031**: Atualização de senha altera hash no banco
- [ ] **RT-032**: Usuário não pode se tornar superuser via PATCH `/users/me`
- [ ] **RT-033**: Usuário não pode se desativar via PATCH `/users/me`
- [ ] **RT-034**: Superuser pode atualizar qualquer usuário
- [ ] **RT-035**: Superuser pode alterar `is_superuser` e `is_active` de outros usuários
- [ ] **RT-036**: Usuário normal não pode atualizar outro usuário
- [ ] **RT-037**: Atualização mantém email original se não fornecido

#### 2.5 Busca de Usuários
- [ ] **RT-038**: Superuser pode buscar usuário por UUID
- [ ] **RT-039**: Busca de usuário inexistente retorna 404
- [ ] **RT-040**: Busca retorna dados corretos do usuário

---

### 3. Gerenciamento de Projetos

#### 3.1 Criação de Projetos
- [ ] **RT-041**: Criar projeto autenticado retorna 200
- [ ] **RT-042**: Criar projeto sem autenticação retorna 401
- [ ] **RT-043**: Criar projeto com dados válidos retorna sucesso
- [ ] **RT-044**: Criar projeto sem campo obrigatório retorna 422
- [ ] **RT-045**: Projeto criado tem `student_id` igual ao UUID do usuário autenticado
- [ ] **RT-046**: Projeto criado tem `timestamp` preenchido
- [ ] **RT-047**: Projeto criado tem `uuid` único gerado
- [ ] **RT-048**: Resposta inclui `project_id_mongo`, `project_uuid` e `timestamp`

#### 3.2 Agregação de Campos
- [ ] **RT-049**: Campos agregados são preenchidos automaticamente quando campos detalhados são fornecidos
- [ ] **RT-050**: `clarity_problem` é agregado de `problem_description`, `target_audience`, `value_proposition`
- [ ] **RT-051**: `tec_eco_viability` é agregado de `technical_feasibility`, `revenue_model`, `scalability`
- [ ] **RT-052**: `application_potencial` é agregado de `customer_segment`, `competitive_advantage`
- [ ] **RT-053**: Campos agregados podem ser fornecidos diretamente (não sobrescrevem)
- [ ] **RT-054**: `inovation_grade` usa `innovation` se fornecido, senão usa campo agregado
- [ ] **RT-055**: `social_impact_aggregated` usa `social_impact` se fornecido

#### 3.3 Campos do Projeto
- [ ] **RT-056**: Criar projeto com todos os 15 campos detalhados funciona
- [ ] **RT-057**: Criar projeto com campos opcionais vazios funciona
- [ ] **RT-058**: Campos pessoais (who_are_you, academy_info, market_info) são salvos corretamente
- [ ] **RT-059**: Campos opcionais podem ser omitidos (retornam string vazia)

#### 3.4 Listagem de Projetos
- [ ] **RT-060**: GET `/projects/` retorna apenas projetos do usuário autenticado
- [ ] **RT-061**: Lista não inclui projetos de outros usuários
- [ ] **RT-062**: Lista retorna array vazio se usuário não tem projetos
- [ ] **RT-063**: Lista retorna todos os campos do projeto

#### 3.5 Detalhes do Projeto
- [ ] **RT-064**: GET `/projects/{uuid}` retorna projeto válido
- [ ] **RT-065**: Buscar projeto inexistente retorna 404
- [ ] **RT-066**: Buscar projeto de outro usuário retorna 403
- [ ] **RT-067**: UUID inválido retorna 400
- [ ] **RT-068**: Detalhes retornam todos os campos do projeto

#### 3.6 Atualização de Projetos
- [ ] **RT-069**: PATCH `/projects/{uuid}` atualiza projeto válido
- [ ] **RT-070**: Atualizar projeto inexistente retorna 404
- [ ] **RT-071**: Atualizar projeto de outro usuário retorna 403
- [ ] **RT-072**: Atualização mantém `student_id` original
- [ ] **RT-073**: Atualização mantém `uuid` original
- [ ] **RT-074**: Atualização atualiza campos agregados corretamente
- [ ] **RT-075**: Resposta de atualização inclui `project_id_mongo`, `project_uuid`, `timestamp`

#### 3.7 Exclusão de Projetos
- [ ] **RT-076**: DELETE `/projects/{uuid}` deleta projeto válido
- [ ] **RT-077**: Deletar projeto inexistente retorna 404
- [ ] **RT-078**: Deletar projeto de outro usuário retorna 403
- [ ] **RT-079**: Projeto deletado não aparece mais na listagem
- [ ] **RT-080**: Resposta de exclusão retorna mensagem de sucesso

---

### 4. Análise de Projetos com IA (Feedback)

#### 4.1 Geração de Análise
- [ ] **RT-081**: POST `/feedback/{project_uuid}` gera análise para projeto válido
- [ ] **RT-082**: Análise de projeto inexistente retorna 404
- [ ] **RT-083**: Análise retorna `feedback_id`, `feedback_summary` e `criteria_evaluation`
- [ ] **RT-084**: Análise é salva no banco de dados
- [ ] **RT-085**: Análise está vinculada ao projeto correto (`project_id`)
- [ ] **RT-086**: Análise está vinculada ao estudante correto (`student_id`)

#### 4.2 Cache de Análise
- [ ] **RT-087**: Análise existente é retornada sem regenerar (sem `regenerate=true`)
- [ ] **RT-088**: `regenerate=true` força nova geração de análise
- [ ] **RT-089**: Análise existente sem `criteria_evaluation` é regenerada automaticamente
- [ ] **RT-090**: Mensagem indica se análise é cacheada ou nova

#### 4.3 Validação de Resposta da IA
- [ ] **RT-091**: Resposta inválida do Gemini retorna erro 500 apropriado
- [ ] **RT-092**: JSON malformado do Gemini é tratado corretamente
- [ ] **RT-093**: Resposta vazia do Gemini retorna erro apropriado
- [ ] **RT-094**: `criteria_evaluation` é validado contra schema
- [ ] **RT-095**: `full_feedback` é string não vazia

#### 4.4 Busca de Feedback
- [ ] **RT-096**: GET `/feedback/{project_uuid}` retorna feedback existente
- [ ] **RT-097**: Buscar feedback inexistente retorna 404
- [ ] **RT-098**: Buscar feedback de projeto de outro usuário retorna 403
- [ ] **RT-099**: Feedback retorna todos os campos incluindo `criteria_evaluation`

#### 4.5 Listagem de Feedbacks
- [ ] **RT-100**: GET `/feedback/user/all` retorna todos os feedbacks do usuário
- [ ] **RT-101**: Lista não inclui feedbacks de outros usuários
- [ ] **RT-102**: Lista retorna array vazio se usuário não tem feedbacks

---

### 5. Geração de Resumos com IA

#### 5.1 Geração de Resumo
- [ ] **RT-103**: GET `/resum/{project_uuid}` gera resumo para projeto válido
- [ ] **RT-104**: Resumo de projeto inexistente retorna 404
- [ ] **RT-105**: Resumo de projeto sem aluno vinculado retorna 404
- [ ] **RT-106**: Resumo retorna `resum_id` e `resums` com 5 campos
- [ ] **RT-107**: Resumo inclui: `clarity_resum`, `inovation_grade_resum`, `social_impact_resum`, `tec_eco_viability_resum`, `application_potencial_resum`
- [ ] **RT-108**: Resumo é salvo no banco de dados (AIResum)
- [ ] **RT-109**: Resumo está vinculado ao projeto correto
- [ ] **RT-110**: Resumo está vinculado ao estudante correto

#### 5.2 Validação de Resposta da IA
- [ ] **RT-111**: Resposta inválida do Gemini retorna erro 500
- [ ] **RT-112**: JSON malformado do Gemini é tratado (limpeza de ```json)
- [ ] **RT-113**: Resposta vazia do Gemini retorna erro apropriado
- [ ] **RT-114**: Resposta sem campo `resums` retorna erro
- [ ] **RT-115**: Todos os 5 campos de resumo estão presentes

---

### 6. Integridade de Dados

#### 6.1 Relacionamentos
- [ ] **RT-116**: Projeto deletado não quebra referências em Feedback
- [ ] **RT-117**: Projeto deletado não quebra referências em AIResum
- [ ] **RT-118**: Usuário deletado (se implementado) não quebra referências em Projetos
- [ ] **RT-119**: UUIDs são únicos em todas as coleções

#### 6.2 Consistência
- [ ] **RT-120**: Timestamps são gerados corretamente
- [ ] **RT-121**: UUIDs são gerados corretamente (formato válido)
- [ ] **RT-122**: Campos obrigatórios não podem ser None após criação
- [ ] **RT-123**: Campos opcionais podem ser None/string vazia

---

### 7. Validações e Tratamento de Erros

#### 7.1 Validação de Entrada
- [ ] **RT-124**: Campos obrigatórios ausentes retornam 422
- [ ] **RT-125**: Tipos incorretos retornam 422
- [ ] **RT-126**: UUIDs inválidos retornam 400
- [ ] **RT-127**: Emails inválidos retornam 422

#### 7.2 Tratamento de Erros
- [ ] **RT-128**: Erros 400 retornam mensagem descritiva
- [ ] **RT-129**: Erros 401 retornam mensagem de não autenticado
- [ ] **RT-130**: Erros 403 retornam mensagem de não autorizado
- [ ] **RT-131**: Erros 404 retornam mensagem de não encontrado
- [ ] **RT-132**: Erros 422 retornam detalhes de validação
- [ ] **RT-133**: Erros 500 retornam mensagem genérica (sem expor detalhes internos)

---

### 8. Performance e Limites

#### 8.1 Performance Básica
- [ ] **RT-134**: Criação de usuário completa em < 1s
- [ ] **RT-135**: Login completa em < 1s
- [ ] **RT-136**: Criação de projeto completa em < 2s
- [ ] **RT-137**: Listagem de projetos completa em < 1s

#### 8.2 Limites
- [ ] **RT-138**: Nome de usuário com comprimento mínimo válido
- [ ] **RT-139**: Email com formato válido
- [ ] **RT-140**: Projeto com campos de texto muito longos (se houver limite)

---

## 🧪 Estratégia de Execução

### Priorização
1. **Crítico (P0)**: Autenticação, CRUD básico de usuários e projetos
2. **Alto (P1)**: Autorização, validações, relacionamentos
3. **Médio (P2)**: Integração com IA, agregação de campos
4. **Baixo (P3)**: Performance, limites, casos extremos

### Ordem de Execução Sugerida
1. Autenticação e Autorização (RT-001 a RT-010)
2. Gerenciamento de Usuários (RT-011 a RT-040)
3. Gerenciamento de Projetos - CRUD básico (RT-041 a RT-080)
4. Análise de Projetos com IA (RT-081 a RT-102)
5. Geração de Resumos com IA (RT-103 a RT-115)
6. Integridade e Validações (RT-116 a RT-140)

### Ambiente de Teste
- **Banco de Dados**: `ConnectInnovaTest` (limpo antes/depois de cada teste)
- **Framework**: pytest com pytest-asyncio
- **Cliente HTTP**: httpx AsyncClient
- **Cobertura**: Mínimo 80% das funcionalidades críticas

---

## 📊 Critérios de Aceitação

### Critérios Gerais
- ✅ Todos os testes P0 (Crítico) devem passar
- ✅ 95% dos testes P1 (Alto) devem passar
- ✅ 90% dos testes P2 (Médio) devem passar
- ✅ 80% dos testes P3 (Baixo) devem passar

### Critérios Específicos
- ✅ Nenhuma regressão em funcionalidades já testadas
- ✅ Todas as validações de segurança funcionando
- ✅ Integridade de dados mantida
- ✅ Performance não degradou significativamente

---

## 📝 Notas de Implementação

### Como Implementar os Testes

Os testes devem ser implementados como funções pytest no formato:

```python
@pytest.mark.anyio
async def test_rt_001_login_com_credenciais_validas(client: AsyncClient) -> None:
    """RT-001: Login com credenciais válidas retorna token de acesso"""
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = await client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    assert r.status_code == status.HTTP_200_OK
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]
```

### Execução Automática

Após implementação, os testes serão executados automaticamente:

```bash
# Executar todos os testes
task test

# Ou diretamente com pytest
uv run pytest

# Executar com cobertura
uv run pytest --cov=app --cov-report=term-missing

# Executar testes específicos
uv run pytest tests/routers/test_users.py
```

### Integração CI/CD

Os testes podem ser integrados em pipelines (GitHub Actions, GitLab CI, etc.) para execução automática em:
- Pull Requests
- Commits na branch main
- Releases
- Agendamento periódico

### Testes Mockados
- **IA (Gemini)**: Considerar mockar chamadas à API Gemini para testes mais rápidos e estáveis
- **Variáveis de Ambiente**: Garantir que `GEMINI_API_KEY` está configurada ou mockada

### Dados de Teste
- Usar funções utilitárias existentes: `create_test_user()`, `create_test_project()`, `random_email()`, etc.
- Limpar banco de dados antes/depois de cada teste (já implementado em `conftest.py`)

### Estrutura de Arquivos Sugerida
```
backend/tests/
├── conftest.py (já existe)
├── utils.py (já existe)
└── routers/
    ├── test_login.py (já existe - expandir)
    ├── test_users.py (já existe - expandir)
    ├── test_project.py (já existe - expandir)
    ├── test_project_new_fields.py (já existe - expandir)
    ├── test_feedback.py (criar)
    ├── test_resum.py (criar)
    └── test_integrity.py (criar)
```

---

## 🔄 Manutenção do Plano

### Revisão Periódica
- Revisar após cada release
- Adicionar novos casos quando novas funcionalidades são implementadas
- Remover casos obsoletos quando funcionalidades são removidas

### Atualização
- Manter sincronizado com mudanças no código
- Documentar decisões de não implementar certos testes
- Priorizar testes baseados em bugs encontrados em produção

---

## 📌 Observações Finais

1. **Testes de IA**: Considerar criar testes com mocks para evitar custos e dependências externas
2. **Testes de Integração**: Alguns testes podem ser considerados testes de integração (ex: com Gemini)
3. **Cobertura**: Usar `pytest-cov` para medir cobertura de código
4. **CI/CD**: Integrar execução automática dos testes de regressão no pipeline

---

**Data de Criação**: 2025
**Última Atualização**: 2025
**Versão**: 1.0
