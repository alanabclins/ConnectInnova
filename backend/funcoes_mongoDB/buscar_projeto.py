from bson.objectid import ObjectId

def buscar_projeto_por_id(projeto_collection, projeto_id_obj):
    """
    Busca um projeto no banco de dados pelo seu _id (já como ObjectId).
    """
    print("   [Passo 1] Buscando projeto no banco de dados...")
    try:
        # A busca real no banco de dados
        projeto = projeto_collection.find_one({"_id": projeto_id_obj})
        
        if not projeto:
            print(f"   [Passo 1] ❌ Projeto com ID {projeto_id_obj} não encontrado")
            return None
        
        print(f"   [Passo 1] ✅ Projeto encontrado: {projeto.get('titulo', 'Sem título')}")
        return projeto

    except Exception as e:
        erro_msg = f"Erro ao buscar projeto com ID {projeto_id_obj}: {e}"
        print(f"   [Passo 1] ❌ {erro_msg}")
        return None