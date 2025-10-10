def buscar_projeto_por_id(Projetos_collection, Projeto_id_obj):
    """
    Busca um projeto no banco de dados pelo seu _id (já como ObjectId).
    """
    print("   [Passo 1] Buscando projeto no banco de dados...")
    try:
        # A busca real no banco de dados
        Projetos = Projetos_collection.find_one({"_id": Projeto_id_obj})
        if not Projetos:
            print(f"   [Passo 1] ❌ Projetos com ID {Projeto_id_obj} não encontrado")
            return None
        print(f"   [Passo 1] ✅ Projetos encontrado: {Projetos.get('titulo', 'Sem título')}")
        return Projetos

    except Exception as e:
        erro_msg = f"Erro ao buscar Projetos com ID {Projeto_id_obj}: {e}"
        print(f"   [Passo 1] ❌ {erro_msg}")
        return None
