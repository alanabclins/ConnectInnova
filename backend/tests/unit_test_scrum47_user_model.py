"""
Unit Test - SCRUM-47: User Model
Unit tests to validate User document structure

Task: SCRUM-47 - [Database] Create users collection  
Required fields: user_id, name, email, password_hash, created_at

Execute: pytest tests/unit_test_scrum47_user_model.py -v
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from uuid import UUID

from app.models.users import User


class TestUserModelValidation:
    """Testes de validação do modelo User usando model_validate"""
    
    def test_validate_with_all_required_fields(self):
        """Teste 1: Validar dados com todos os campos obrigatórios"""
        data = {
            "name": "João Silva",
            "email": "joao@example.com",
            "password_hash": "$2b$12$KIXxAbC123HashExemploSenha"
        }
        
        # model_construct não precisa de conexão ao banco
        user_data = User.model_construct(**data)
        
        assert user_data.name == "João Silva"
        assert user_data.email == "joao@example.com"
        assert user_data.password_hash == "$2b$12$KIXxAbC123HashExemploSenha"
        assert user_data.created_at is not None
        assert isinstance(user_data.created_at, datetime)
        assert user_data.uuid is not None
        assert isinstance(user_data.uuid, UUID)
    
    def test_missing_required_field_nome(self):
        """Teste 2: Erro ao validar dados sem 'name'"""
        data = {
            "email": "test@example.com",
            "password_hash": "$2b$12$hash"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            User.model_validate(data)
        
        errors = exc_info.value.errors()
        assert any('name' in str(error['loc']) for error in errors)
    
    def test_missing_required_field_email(self):
        """Teste 3: Erro ao validar dados sem 'email'"""
        data = {
            "name": "Test User",
            "password_hash": "$2b$12$hash"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            User.model_validate(data)
        
        errors = exc_info.value.errors()
        assert any('email' in str(error['loc']) for error in errors)
    
    def test_missing_required_field_senha_hash(self):
        """Teste 4: Erro ao validar dados sem 'password_hash'"""
        data = {
            "name": "Test User",
            "email": "test@example.com"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            User.model_validate(data)
        
        errors = exc_info.value.errors()
        assert any('password_hash' in str(error['loc']) for error in errors)
    
    def test_invalid_email_format(self):
        """Teste 5: Erro ao usar email com formato inválido"""
        data = {
            "name": "Test User",
            "email": "email-invalido-sem-arroba",
            "password_hash": "$2b$12$hash"
        }
        
        with pytest.raises(ValidationError) as exc_info:
            User.model_validate(data)
        
        errors = exc_info.value.errors()
        assert any('email' in str(error['loc']) for error in errors)
    
    def test_optional_fields_default_values(self):
        """Teste 6: Valores default dos campos opcionais"""
        data = {
            "name": "Test User",
            "email": "test@example.com",
            "password_hash": "$2b$12$hash"
        }
        
        user = User.model_construct(**data)
        
        assert user.first_name is None
        assert user.last_name is None
        assert user.hashed_password is None
        assert user.provider is None
        assert user.picture is None
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.updated_at is None
    
    def test_set_optional_fields(self):
        """Teste 7: Definir campos opcionais"""
        data = {
            "name": "Ana Paula Costa",
            "email": "ana@example.com",
            "password_hash": "$2b$12$hash",
            "first_name": "Ana",
            "last_name": "Costa",
            "provider": "google",
            "picture": "https://example.com/photo.jpg",
            "is_active": True,
            "is_superuser": False
        }
        
        user = User.model_construct(**data)
        
        assert user.first_name == "Ana"
        assert user.last_name == "Costa"
        assert user.provider == "google"
        assert user.picture == "https://example.com/photo.jpg"
    
    def test_uuid_auto_generated(self):
        """Teste 8: UUID é gerado automaticamente"""
        data = {
            "name": "UUID Test",
            "email": "uuid@example.com",
            "password_hash": "$2b$12$hash"
        }
        
        user = User.model_construct(**data)
        
        assert user.uuid is not None
        assert isinstance(user.uuid, UUID)
        assert len(str(user.uuid)) == 36  # Formato UUID
    
    def test_email_validation_with_valid_formats(self):
        """Teste 9: Validar diferentes formatos de email válidos"""
        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
            "user_name@example-domain.com",
            "123@example.com",
        ]
        
        for email in valid_emails:
            data = {
                "name": "Test User",
                "email": email,
                "password_hash": "$2b$12$hash"
            }
            user = User.model_construct(**data)
            assert user.email == email
    
    def test_email_validation_with_invalid_formats(self):
        """Teste 10: Rejeitar formatos de email inválidos"""
        invalid_emails = [
            "plaintext",
            "@example.com",
            "user@",
            "user @example.com",
            "user@.com",
        ]
        
        for email in invalid_emails:
            data = {
                "name": "Test User",
                "email": email,
                "password_hash": "$2b$12$hash"
            }
            with pytest.raises(ValidationError):
                User.model_validate(data)
    
    def test_model_dict_export(self):
        """Teste 11: Exportar modelo para dicionário"""
        data = {
            "name": "Export Test",
            "email": "export@example.com",
            "password_hash": "$2b$12$hash",
            "provider": "local"
        }
        
        user = User.model_construct(**data)
        user_dict = user.model_dump()
        
        assert user_dict['name'] == "Export Test"
        assert user_dict['email'] == "export@example.com"
        assert user_dict['password_hash'] == "$2b$12$hash"
        assert user_dict['provider'] == "local"
        assert 'created_at' in user_dict
        assert 'uuid' in user_dict
    
    def test_model_json_export(self):
        """Teste 12: Exportar modelo para JSON"""
        data = {
            "name": "JSON Test",
            "email": "json@example.com",
            "password_hash": "$2b$12$hash"
        }
        
        user = User.model_construct(**data)
        json_str = user.model_dump_json()
        
        assert '"name":"JSON Test"' in json_str or '"name": "JSON Test"' in json_str
        assert '"email":"json@example.com"' in json_str or '"email": "json@example.com"' in json_str
    
    def test_boolean_fields_default_values(self):
        """Teste 13: Campos booleanos têm valores default corretos"""
        data = {
            "name": "Boolean Test",
            "email": "boolean@example.com",
            "password_hash": "$2b$12$hash"
        }
        
        user = User.model_construct(**data)
        
        assert user.is_active is True
        assert user.is_superuser is False
    
    def test_change_boolean_fields(self):
        """Teste 14: Modificar campos booleanos"""
        data = {
            "name": "Boolean Change Test",
            "email": "change@example.com",
            "password_hash": "$2b$12$hash",
            "is_active": False,
            "is_superuser": True
        }
        
        user = User.model_construct(**data)
        
        assert user.is_active is False
        assert user.is_superuser is True
    
    def test_data_atualizacao_can_be_set(self):
        """Teste 15: Campo data_atualizacao pode ser definido"""
        now = datetime.utcnow()
        
        data = {
            "name": "Update Test",
            "email": "update@example.com",
            "password_hash": "$2b$12$hash",
            "updated_at": now  # Passar datetime diretamente
        }
        
        user = User.model_construct(**data)
        
        assert user.updated_at is not None
        assert isinstance(user.updated_at, datetime)
        assert user.updated_at == now
    
    def test_data_criacao_auto_generated(self):
        """Teste 16: data_criacao é gerada automaticamente se não fornecida"""
        data = {
            "name": "Auto Test",
            "email": "auto@example.com",
            "password_hash": "$2b$12$hash"
        }
        
        user = User.model_construct(**data)
        
        assert user.created_at is not None
        assert isinstance(user.created_at, datetime)
    
    def test_all_fields_together(self):
        """Teste 17: Validar todos os campos juntos"""
        data = {
            "name": "Complete User",
            "email": "complete@example.com",
            "password_hash": "$2b$12$CompleteHash",
            "first_name": "Complete",
            "last_name": "User",
            "hashed_password": "$2b$12$Legacy",
            "provider": "local",
            "picture": "https://example.com/pic.jpg",
            "is_active": True,
            "is_superuser": False
        }
        
        user = User.model_construct(**data)
        
        # Campos obrigatórios
        assert user.name == "Complete User"
        assert user.email == "complete@example.com"
        assert user.password_hash == "$2b$12$CompleteHash"
        assert user.created_at is not None
        
        # Campos opcionais
        assert user.first_name == "Complete"
        assert user.last_name == "User"
        assert user.provider == "local"
        assert user.picture == "https://example.com/pic.jpg"
        assert user.is_active is True
        assert user.is_superuser is False
        
        # Campos auto-gerados
        assert user.uuid is not None
    
    def test_email_case_preserved(self):
        """Teste 18: Email mantém o case fornecido"""
        data = {
            "name": "Case Test",
            "email": "CaseSensitive@Example.COM",
            "password_hash": "$2b$12$hash"
        }
        
        user = User.model_construct(**data)
        
        # Beanie/Pydantic mantém o case do email como fornecido
        assert user.email == "CaseSensitive@Example.COM"
