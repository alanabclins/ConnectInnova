def gerar_prompt_analise(projeto):
    """Gera o prompt estruturado para análise do projeto."""
    print("   [Task 33] Gerando prompt para a IA...")
    titulo = projeto.get('titulo', 'N/A')
    resumo = projeto.get('resumo', 'N/A')

    prompt = f"""
    # CONTEXTO
    Você é a "IA Orientadora", uma especialista em avaliar projetos acadêmicos de inovação. Sua tarefa é fornecer um feedback geral sobre o projeto submetido
    # TEXTO DO PROJETO PARA ANÁLISE
    - Título: "{titulo}"
    - Resumo: "{resumo}"

    # TAREFA
    Com base no texto fornecido, gere um feedback em formato de objeto JSON que siga. Não adicione nenhum texto ou explicação antes ou depois do JSON.
    """
    print("   [Task 33] ✅ Prompt gerado.")
    return prompt