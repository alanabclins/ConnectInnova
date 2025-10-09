from db_connection import Projetos_collection, Alunos_collection
from bson.objectid import ObjectId
from datetime import datetime

def criar_projeto(payload):
    """
    Cria um novo projeto no MongoDB e retorna o ID inserido.
    Evita duplicações com base no título do projeto.
    """
    try:
        # Verifica se já existe projeto com o mesmo título
        existente = Projetos_collection.find_one({"project_title": payload["project_title"]})
        if existente:
            print(f"⚠️ Projeto '{payload['project_title']}' já existe no banco.")
            return existente["_id"]

        # Verifica se o aluno já existe
        estudante = Alunos_collection.find_one({"name": payload["student_name"]})
        if not estudante:
            estudante_id = Alunos_collection.insert_one({
                "name": payload["student_name"],
                "student_description": payload.get("student_description", ""),
                "skills_experiencies": payload.get("student_skills", ""),
                "curriculum": None,
                "academic_informations": "",
            }).inserted_id
        else:
            estudante_id = estudante["_id"]

        # Cria o projeto vinculado ao aluno
        projeto = {
            "project_title": payload["project_title"],
            "project_description": payload["project_description"],
            "solution_proposal": payload["solution_proposal"],
            "student_id": ObjectId(estudante_id),
            "timestamp": datetime.utcnow(),
            "clarity_problem": payload["clarity_problem"],
            "inovation_grade": payload["inovation_grade"],
            "social_impact": payload["social_impact"],
            "tec_eco_viability": payload["tec_eco_viability"],
            "application_potencial": payload["application_potencial"]
        }
        resultado = Projetos_collection.insert_one(projeto)
        print(f"✅ Projeto '{payload['project_title']}' criado com sucesso.")
        return resultado.inserted_id

    except Exception as e:
        print(f"❌ Erro ao criar projeto: {e}")
        return None
