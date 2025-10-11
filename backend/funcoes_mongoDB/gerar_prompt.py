def gerar_prompt_analise(projeto):
    titulo = projeto.get("project_title", "Sem título")
    descricao = projeto.get("project_description", "Sem descrição")
    proposta = projeto.get("solution_proposal", "Sem proposta")
    impacto = projeto.get("social_impact", "Sem impacto")
    viabilidade = projeto.get("tec_eco_viability", "Sem viabilidade")
    inovacao = projeto.get("inovation_grade", "Sem inovação")
    aplicacao = projeto.get("application_potencial", "Sem potencial")

    prompt = f"""
Você é um avaliador de projetos universitários. Avalie o seguinte projeto com base nas
dimensões abaixo:

Título: {titulo}
Descrição do Problema: {descricao}
Proposta de Solução: {proposta}
Impacto Social: {impacto}
Viabilidade Técnica e Econômica: {viabilidade}
Grau de Inovação: {inovacao}
Potencial de Aplicação: {aplicacao}

Responda SOMENTE em formato JSON, com as seguintes chaves (sem texto adicional fora do JSON):

{{
  "clarity_problem": "avaliação da clareza do problema (máx 2 frases)",
  "inovation_grade": "avaliação do grau de inovação (máx 2 frases)",
  "social_impact": "avaliação do impacto social (máx 2 frases)",
  "tec_eco_viability": "avaliação da viabilidade técnica e econômica 
  (máx 2 frases)",
  "application_potencial": "avaliação do potencial de aplicação (máx 2 frases)"
  "solution_proposal" : "avaliação da proposta de solução (máx 2 frases)
}}
"""
    return prompt.strip()


def gerar_prompt_resumo(projeto):
    titulo = projeto.get("project_title", "Sem título")
    descricao = projeto.get("project_description", "Sem descrição")
    proposta = projeto.get("solution_proposal", "Sem proposta")
    impacto = projeto.get("social_impact", "Sem impacto")
    viabilidade = projeto.get("tec_eco_viability", "Sem viabilidade")
    inovacao = projeto.get("inovation_grade", "Sem inovação")
    aplicacao = projeto.get("application_potencial", "Sem potencial")

    prompt = f"""
Elabore um resumo de cada ponto do projeto, baseado no que foi descrito nos quesitos:

Título : {titulo}
Descrição do Problema: {descricao}
Proposta de Solução: {proposta}
Impacto Social: {impacto}
Viabilidade Técnica e Econômica: {viabilidade}
Grau de Inovação: {inovacao}
Potencial de Aplicação: {aplicacao}

Responda SOMENTE em formato JSON, com as seguintes chaves (sem texto adicional fora do JSON):

{{
  "clarity_problem": "resumo da clareza do problema na qual o projeto foca (1 palavra chave)",
  "inovation_grade": "resumo de como se dá o grau de inovação do projeto (1 palavra chave)",
  "social_impact": "resumo de como o projeto impactará socialmente (1 palavra chave)",
  "tec_eco_viability": "resumo de como se dá a viabilidade técnica e
  econômica do projeto (1 palavra chave)",
  "application_potencial": "resumo do potencial de aplicação do projeto (1 palavra chave)"
  "solution_proposal": "resumo da proposta de solução do projeto (1 palavra chave)"
}}
"""
    return prompt.strip()
