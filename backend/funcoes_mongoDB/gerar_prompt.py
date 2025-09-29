def gerar_prompt_analise(projeto):
    """Gera o prompt estruturado para análise geral do projeto."""
    print("   [Task 33] Gerando prompt para a IA...")
    
    # Extrai todos os campos necessários do projeto
    titulo = projeto.get('titulo', 'N/A')
    descricao_problema = projeto.get('descricao_problema', 'N/A')
    proposta_solucao = projeto.get('proposta_solucao', 'N/A')
    impacto_social = projeto.get('impacto_social', 'N/A')
    viabilidade_tecnica = projeto.get('viabilidade_tecnica', 'N/A')
    inovacao = projeto.get('inovacao', 'N/A')

    prompt = f"""
# CONTEXTO
Você é a "IA Orientadora", uma especialista em avaliar projetos acadêmicos de inovação. 
Sua tarefa é fornecer uma análise geral e livre sobre o projeto submetido.

# DADOS DO PROJETO PARA ANÁLISE
- Título: "{titulo}"
- Descrição do Problema: "{descricao_problema}"
- Proposta de Solução: "{proposta_solucao}"
- Impacto Social Esperado: "{impacto_social}"
- Viabilidade Técnica e Econômica: "{viabilidade_tecnica}"
- Inovação do Projeto: "{inovacao}"

# TAREFA
Com base nas informações fornecidas acima, faça uma análise geral e livre da proposta do projeto. 
Forneça um feedback textual coeso que avalie a proposta de forma abrangente, considerando 
aspectos como clareza, inovação, impacto social, viabilidade e potencial de aplicação.

Retorne apenas o texto da análise, sem formatação especial ou estruturas pré-definidas.
"""
    print("   [Task 33] ✅ Prompt gerado.")
    return prompt
