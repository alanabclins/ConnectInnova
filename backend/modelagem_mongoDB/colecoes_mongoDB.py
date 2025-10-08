from pymongo import MongoClient
import os

# Configuração da conexão
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB = os.getenv("MONGO_DB", "ConnectInnova")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

# -------------------------------
# 1. Coleção STUDENTS
# -------------------------------
if 'Students' in db.list_collection_names():
    db.drop_collection('Students')

db.create_collection('Students', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'name',
            'student_description',
            'curriculum',
            'academic_informations',
            'skills_experiencies'
        ],
        'properties': {
            'name': {'bsonType': 'string'},
            'student_description': {'bsonType': 'string'},
            'curriculum': {'bsonType': ['string', 'null']},
            'academic_informations': {'bsonType': 'string'},
            'skills_experiencies': {'bsonType': 'string'}
        }
    }
})
print("✅ Coleção 'Students' criada com sucesso!")


# -------------------------------
# 2. Coleção PROJECTS
# -------------------------------
if 'Projects' in db.list_collection_names():
    db.drop_collection('Projects')

db.create_collection('Projects', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'project_title',
            'project_description',
            'solution_proposal',
            'student_id'
        ],
        'properties': {
            'project_title': {'bsonType': 'string'},
            'project_description': {'bsonType': 'string'},
            'solution_proposal': {'bsonType': 'string'},
            'student_id': {'bsonType': 'objectId'},
            # 'feedback_id': {
            #     'bsonType': ['objectId', 'null'],
            #     "description": "ID do feedback relacionado ao projeto",
            #     'properties': {
            #         'content': {'bsonType': 'string'},
            #         'status': {'bsonType': 'string'},
            #         'timestamp': {'bsonType': 'date'}
            #     }
            # },
            'clarity_problem': {'bsonType': ['string', 'null']},
            'inovation_grade': {'bsonType': ['string', 'null']},
            'social_impact': {'bsonType': ['string', 'null']},
            'tec_eco_viability': {'bsonType': ['string', 'null']},
            'application_potencial': {'bsonType': ['string', 'null']}
        }
    }
})
print("✅ Coleção 'Projects' criada com sucesso!")


# -------------------------------
# 3. Coleção FEEDBACK
# -------------------------------
if 'Feedback' in db.list_collection_names():
    db.drop_collection('Feedback')

db.create_collection('Feedback', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'project_id',
            'student_id',
            'feedback',
        ],
        'properties': {
            'feedback': {
                'bsonType': ['object', 'null'],
                'properties': {
                    'content': {'bsonType': 'string'},
                    'status': {'bsonType': 'string'},
                    'timestamp': {'bsonType': 'date'}
                }
            },
            'project_id': {
                'bsonType': 'objectId',
                'description': 'Referência ao projeto avaliado'
            },
            'student_id': {
                'bsonType': ['objectId', 'null'],
                'description': 'Referência ao aluno na coleção Students'
            },
            'ai_feedback_clarity_problem': {
                'bsonType': ['string', 'null'],
                'description': 'Avaliação da IA sobre a clareza do problema'
            },
            'ai_feedback_inovation_grade': {
                'bsonType': ['string', 'null'],
                'description': 'Avaliação da IA sobre o grau de inovação'
            },
            'ai_feedback_social_impact': {
                'bsonType': ['string', 'null'],
                'description': 'Avaliação da IA sobre o impacto social'
            },
            'ai_feedback_tec_eco_viability': {
                'bsonType': ['string', 'null'],
                'description': 'Avaliação da IA sobre a viabilidade técnica e econômica'
            },
            'ai_feedback_application_potencial': {
                'bsonType': ['string', 'null'],
                'description': 'Avaliação da IA sobre o potencial de aplicação'
            }
        }
    }
})
print("✅ Coleção 'Feedback' criada com sucesso!")



# -------------------------------
# 4. Coleção AI_RESUM
# -------------------------------
if 'AI_Resum' in db.list_collection_names():
    db.drop_collection('AI_Resum')

db.create_collection('AI_Resum', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'project_id',
            'student_id',
            'clarity_resum',
            'inovation_grade_resum',
            'social_impact_resum',
            'tec_eco_viability_resum',
            'application_potencial_resum'
        ],
        'properties': {
            'project_id': {
                'bsonType': 'objectId',
                'description': 'Referência ao projeto avaliado'
            },
            'student_id': {
                'bsonType': 'objectId',
                'description': 'Referência ao aluno na coleção Students'
            },
            'clarity_resum': {
                'bsonType': 'string',
                'description': 'Resumo da IA sobre a clareza do problema'
            },
            'inovation_grade_resum': {
                'bsonType': 'string',
                'description': 'Resumo da IA sobre o grau de inovação'
            },
            'social_impact_resum': {
                'bsonType': 'string',
                'description': 'Resumo da IA sobre o impacto social'
            },
            'tec_eco_viability_resum': {
                'bsonType': 'string',
                'description': 'Resumo da IA sobre a viabilidade técnica e econômica'
            },
            'application_potencial_resum': {
                'bsonType': 'string',
                'description': 'Resumo da IA sobre o potencial de aplicação'
            }
        }
    }
})
print("✅ Coleção 'AI_Resum' criada com sucesso!")


# -------------------------------
# 5. Coleção USUARIOS
# -------------------------------
if 'Usuarios' in db.list_collection_names():
    db.drop_collection('Usuarios')

db.create_collection('Usuarios', validator={
    '$jsonSchema': {
        'bsonType': 'object',
        'required': [
            'nome',
            'email',
            'senha_hash',
            'data_criacao'
        ],
        'properties': {
            'nome': {
                'bsonType': 'string',
                'description': 'Nome completo do usuário'
            },
            'email': {
                'bsonType': 'string',
                'pattern': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$',
                'description': 'Email único do usuário'
            },
            'senha_hash': {
                'bsonType': 'string',
                'description': 'Hash da senha (bcrypt/argon2)'
            },
            'data_criacao': {
                'bsonType': 'date',
                'description': 'Data de criação do registro'
            },
            'data_atualizacao': {
                'bsonType': ['date', 'null'],
                'description': 'Data da última atualização'
            },
            'is_active': {
                'bsonType': 'bool',
                'description': 'Status ativo/inativo do usuário'
            },
            'provider': {
                'bsonType': ['string', 'null'],
                'description': 'Provedor de autenticação (local, google, github)'
            },
            'picture': {
                'bsonType': ['string', 'null'],
                'description': 'URL da foto de perfil'
            }
        }
    }
})

# Criar índices
usuarios_collection = db['Usuarios']
usuarios_collection.create_index('email', unique=True)
usuarios_collection.create_index('data_criacao')

print("✅ Coleção 'Usuarios' criada com sucesso!")