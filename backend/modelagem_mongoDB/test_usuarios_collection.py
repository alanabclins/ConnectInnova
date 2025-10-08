"""
Script de teste para validar a coleção Usuarios
Execute: python -m modelagem_mongoDB.test_usuarios_collection
"""
import sys
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import WriteError, DuplicateKeyError
import os

# Configuração da conexão
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "ConnectInnova")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
usuarios_collection = db["Usuarios"]

print("=" * 60)
print("🧪 TESTES DA COLEÇÃO USUARIOS")
print("=" * 60)

# Contador de testes
tests_passed = 0
tests_failed = 0

def test_result(test_name, passed, message=""):
    global tests_passed, tests_failed
    if passed:
        tests_passed += 1
        print(f"✅ {test_name}")
        if message:
            print(f"   → {message}")
    else:
        tests_failed += 1
        print(f"❌ {test_name}")
        if message:
            print(f"   → {message}")
    print()


# -------------------------------
# TESTE 1: Verificar se a coleção existe
# -------------------------------
print("\n📋 TESTE 1: Verificar existência da coleção")
collection_exists = "Usuarios" in db.list_collection_names()
test_result(
    "Coleção 'Usuarios' existe no banco de dados",
    collection_exists,
    f"Coleções disponíveis: {db.list_collection_names()}"
)

if not collection_exists:
    print("⚠️  Execute primeiro: python -m modelagem_mongoDB.colecoes_mongoDB")
    sys.exit(1)


# -------------------------------
# TESTE 2: Verificar índices
# -------------------------------
print("📋 TESTE 2: Verificar índices criados")
indexes = list(usuarios_collection.list_indexes())
index_names = [idx['name'] for idx in indexes]

has_email_index = any('email' in idx_name for idx_name in index_names)
test_result(
    "Índice único no campo 'email' existe",
    has_email_index,
    f"Índices encontrados: {index_names}"
)


# -------------------------------
# TESTE 3: Inserir usuário VÁLIDO
# -------------------------------
print("📋 TESTE 3: Inserir documento VÁLIDO")
usuario_valido = {
    "nome": "Alan Alins Teste",
    "email": "teste@connectinnova.com",
    "senha_hash": "$2b$12$KIXxAbC123HashExemploSenhaSegura",
    "data_criacao": datetime.utcnow(),
    "data_atualizacao": None,
    "is_active": True,
    "provider": "local",
    "picture": None
}

try:
    # Limpar teste anterior se existir
    usuarios_collection.delete_one({"email": "teste@connectinnova.com"})
    
    result = usuarios_collection.insert_one(usuario_valido)
    test_result(
        "Inserção de usuário válido com todos os campos",
        result.inserted_id is not None,
        f"ID inserido: {result.inserted_id}"
    )
except Exception as e:
    test_result(
        "Inserção de usuário válido com todos os campos",
        False,
        f"Erro: {str(e)}"
    )


# -------------------------------
# TESTE 4: Tentar inserir SEM campo obrigatório (nome)
# -------------------------------
print("📋 TESTE 4: Validação - Rejeitar documento SEM 'nome'")
usuario_sem_nome = {
    "email": "semNome@test.com",
    "senha_hash": "$2b$12$hash",
    "data_criacao": datetime.utcnow()
}

try:
    usuarios_collection.insert_one(usuario_sem_nome)
    test_result(
        "Schema rejeitou documento sem campo 'nome'",
        False,
        "ERRO: Documento foi aceito quando deveria ser rejeitado!"
    )
except WriteError as e:
    test_result(
        "Schema rejeitou documento sem campo 'nome'",
        True,
        "Validação funcionou corretamente"
    )


# -------------------------------
# TESTE 5: Tentar inserir SEM campo obrigatório (email)
# -------------------------------
print("📋 TESTE 5: Validação - Rejeitar documento SEM 'email'")
usuario_sem_email = {
    "nome": "Usuário Sem Email",
    "senha_hash": "$2b$12$hash",
    "data_criacao": datetime.utcnow()
}

try:
    usuarios_collection.insert_one(usuario_sem_email)
    test_result(
        "Schema rejeitou documento sem campo 'email'",
        False,
        "ERRO: Documento foi aceito quando deveria ser rejeitado!"
    )
except WriteError as e:
    test_result(
        "Schema rejeitou documento sem campo 'email'",
        True,
        "Validação funcionou corretamente"
    )


# -------------------------------
# TESTE 6: Tentar inserir email DUPLICADO
# -------------------------------
print("📋 TESTE 6: Validação - Rejeitar email duplicado")
usuario_duplicado = {
    "nome": "Outro Usuário",
    "email": "teste@connectinnova.com",  # Email já usado no teste 3
    "senha_hash": "$2b$12$hash",
    "data_criacao": datetime.utcnow()
}

try:
    usuarios_collection.insert_one(usuario_duplicado)
    test_result(
        "Índice único rejeitou email duplicado",
        False,
        "ERRO: Email duplicado foi aceito!"
    )
except DuplicateKeyError as e:
    test_result(
        "Índice único rejeitou email duplicado",
        True,
        "Unicidade do email funcionou corretamente"
    )


# -------------------------------
# TESTE 7: Validação de email com padrão inválido
# -------------------------------
print("📋 TESTE 7: Validação - Rejeitar formato de email inválido")
usuario_email_invalido = {
    "nome": "Usuário Email Inválido",
    "email": "email-invalido-sem-arroba",
    "senha_hash": "$2b$12$hash",
    "data_criacao": datetime.utcnow()
}

try:
    usuarios_collection.insert_one(usuario_email_invalido)
    test_result(
        "Schema rejeitou email com formato inválido",
        False,
        "ERRO: Email inválido foi aceito!"
    )
except WriteError as e:
    test_result(
        "Schema rejeitou email com formato inválido",
        True,
        "Validação de padrão de email funcionou"
    )


# -------------------------------
# TESTE 8: Inserir com campos opcionais nulos
# -------------------------------
print("📋 TESTE 8: Inserir documento com campos opcionais NULL")
usuario_minimo = {
    "nome": "Usuário Mínimo",
    "email": "minimo@test.com",
    "senha_hash": "$2b$12$hash",
    "data_criacao": datetime.utcnow(),
    "data_atualizacao": None,
    "provider": None,
    "picture": None
}

try:
    usuarios_collection.delete_one({"email": "minimo@test.com"})
    result = usuarios_collection.insert_one(usuario_minimo)
    test_result(
        "Campos opcionais NULL aceitos corretamente",
        result.inserted_id is not None,
        f"ID inserido: {result.inserted_id}"
    )
except Exception as e:
    test_result(
        "Campos opcionais NULL aceitos corretamente",
        False,
        f"Erro: {str(e)}"
    )


# -------------------------------
# TESTE 9: Consultar usuários criados
# -------------------------------
print("📋 TESTE 9: Consultar documentos inseridos")
try:
    count = usuarios_collection.count_documents({})
    usuarios = list(usuarios_collection.find().limit(5))
    
    test_result(
        f"Consulta de documentos ({count} encontrados)",
        count >= 0,
        f"Total de usuários no banco: {count}"
    )
    
    if usuarios:
        print("   📄 Amostra de documentos:")
        for user in usuarios[:3]:
            print(f"      • {user.get('nome')} - {user.get('email')}")
except Exception as e:
    test_result(
        "Consulta de documentos",
        False,
        f"Erro: {str(e)}"
    )


# -------------------------------
# LIMPEZA: Remover dados de teste
# -------------------------------
print("\n🧹 Limpeza de dados de teste...")
try:
    usuarios_collection.delete_many({
        "email": {"$in": [
            "teste@connectinnova.com",
            "minimo@test.com"
        ]}
    })
    print("✅ Dados de teste removidos")
except Exception as e:
    print(f"⚠️  Erro na limpeza: {e}")


# -------------------------------
# RESULTADO FINAL
# -------------------------------
print("\n" + "=" * 60)
print("📊 RESULTADO DOS TESTES")
print("=" * 60)
print(f"✅ Testes Aprovados: {tests_passed}")
print(f"❌ Testes Falhados: {tests_failed}")
print(f"📈 Taxa de Sucesso: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")
print("=" * 60)

if tests_failed == 0:
    print("\n🎉 TODOS OS TESTES PASSARAM! A coleção está funcionando corretamente.")
    sys.exit(0)
else:
    print("\n⚠️  ALGUNS TESTES FALHARAM. Verifique a implementação.")
    sys.exit(1)

