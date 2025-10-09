"""
Unit Test - SCRUM-48: Email Uniqueness
Unit tests to validate email unique index and duplicate prevention

Task: SCRUM-48 - [Database] Guarantee email field uniqueness
Configure unique index to prevent duplicate records

Execute: pytest tests/unit_test_scrum48_email_uniqueness.py -v
"""
import pytest
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from beanie.exceptions import RevisionIdWasChanged

from app.models.users import User


pytestmark = pytest.mark.anyio


@pytest.fixture
async def db():
    """Fixture for test database connection"""
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    database = client.ConnectInnova_Test_EmailUniqueness
    
    # Initialize Beanie
    await init_beanie(database=database, document_models=[User])
    
    yield database
    
    # Cleanup: remove test database
    await client.drop_database("ConnectInnova_Test_EmailUniqueness")
    client.close()


@pytest.fixture(autouse=True)
async def cleanup_collection(db):
    """Clean collection before each test"""
    await User.delete_all()
    yield
    await User.delete_all()


class TestEmailUniqueIndex:
    """Tests for email unique index configuration"""
    
    async def test_email_index_exists(self, db):
        """Test 1: Verify email index exists in collection"""
        collection = db.User
        indexes = await collection.list_indexes().to_list(length=None)
        
        email_index = None
        for idx in indexes:
            if 'email' in idx.get('key', {}):
                email_index = idx
                break
        
        assert email_index is not None, "Email index not found"
        assert 'email_1' in email_index['name']
    
    async def test_email_index_is_unique(self, db):
        """Test 2: Verify email index has unique constraint"""
        collection = db.User
        indexes = await collection.list_indexes().to_list(length=None)
        
        email_index = None
        for idx in indexes:
            if 'email' in idx.get('key', {}):
                email_index = idx
                break
        
        assert email_index is not None
        assert email_index.get('unique') is True, "Email index is not unique"


class TestEmailDuplicatePrevention:
    """Tests for duplicate email prevention"""
    
    async def test_insert_user_with_unique_email(self, db):
        """Test 3: Successfully insert user with unique email"""
        user = User(
            name="John Doe",
            email="john@example.com",
            password_hash="$2b$12$hash"
        )
        
        await user.insert()
        
        assert user.id is not None
        assert user.email == "john@example.com"
    
    async def test_reject_duplicate_email(self, db):
        """Test 4: Reject insertion of duplicate email"""
        # Insert first user
        user1 = User(
            name="John Doe",
            email="duplicate@example.com",
            password_hash="$2b$12$hash1"
        )
        await user1.insert()
        
        # Try to insert second user with same email
        user2 = User(
            name="Jane Doe",
            email="duplicate@example.com",
            password_hash="$2b$12$hash2"
        )
        
        with pytest.raises(DuplicateKeyError):
            await user2.insert()
    
    async def test_multiple_users_different_emails(self, db):
        """Test 5: Allow multiple users with different emails"""
        users = [
            User(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password_hash=f"$2b$12$hash{i}"
            )
            for i in range(5)
        ]
        
        for user in users:
            await user.insert()
        
        count = await User.count()
        assert count == 5
    
    async def test_case_sensitive_emails(self, db):
        """Test 6: Emails are case-sensitive by default"""
        user1 = User(
            name="User 1",
            email="Test@Example.com",
            password_hash="$2b$12$hash1"
        )
        await user1.insert()
        
        user2 = User(
            name="User 2",
            email="test@example.com",  # Different case
            password_hash="$2b$12$hash2"
        )
        await user2.insert()  # Should succeed (case-sensitive)
        
        count = await User.count()
        assert count == 2


class TestEmailValidation:
    """Tests for email format validation"""
    
    async def test_valid_email_formats(self, db):
        """Test 7: Accept valid email formats"""
        valid_emails = [
            "simple@example.com",
            "user.name@example.com",
            "user+tag@example.co.uk",
        ]
        
        for i, email in enumerate(valid_emails):
            user = User(
                name=f"User {i}",
                email=email,
                password_hash="$2b$12$hash"
            )
            await user.insert()
        
        count = await User.count()
        assert count == len(valid_emails)
    
    async def test_invalid_email_format_rejected(self, db):
        """Test 8: Reject invalid email formats"""
        with pytest.raises(ValidationError):
            user = User(
                name="Invalid User",
                email="not-an-email",
                password_hash="$2b$12$hash"
            )


class TestEmailUpdateOperations:
    """Tests for email update scenarios"""
    
    async def test_update_to_existing_email_fails(self, db):
        """Test 9: Prevent updating email to one that already exists"""
        # Insert two users
        user1 = User(
            name="User 1",
            email="user1@example.com",
            password_hash="$2b$12$hash1"
        )
        await user1.insert()
        
        user2 = User(
            name="User 2",
            email="user2@example.com",
            password_hash="$2b$12$hash2"
        )
        await user2.insert()
        
        # Try to update user2's email to user1's email
        user2.email = "user1@example.com"
        
        # Beanie wraps DuplicateKeyError in RevisionIdWasChanged
        with pytest.raises((DuplicateKeyError, RevisionIdWasChanged)):
            await user2.save()
    
    async def test_update_user_keep_same_email(self, db):
        """Test 10: Allow updating other fields keeping same email"""
        user = User(
            name="Original Name",
            email="test@example.com",
            password_hash="$2b$12$hash"
        )
        await user.insert()
        
        # Update name, keep email
        user.name = "Updated Name"
        await user.save()
        
        # Verify update
        updated_user = await User.get(user.id)
        assert updated_user.name == "Updated Name"
        assert updated_user.email == "test@example.com"
    
    async def test_update_email_to_new_unique_value(self, db):
        """Test 11: Allow updating email to a new unique value"""
        user = User(
            name="Test User",
            email="old@example.com",
            password_hash="$2b$12$hash"
        )
        await user.insert()
        
        # Update to new unique email
        user.email = "new@example.com"
        await user.save()
        
        # Verify update
        updated_user = await User.get(user.id)
        assert updated_user.email == "new@example.com"


class TestEmailDeleteOperations:
    """Tests for delete and re-insert scenarios"""
    
    async def test_delete_and_reinsert_same_email(self, db):
        """Test 12: Allow reinserting email after deletion"""
        # Insert user
        user1 = User(
            name="User 1",
            email="reinsert@example.com",
            password_hash="$2b$12$hash1"
        )
        await user1.insert()
        user1_id = user1.id
        
        # Delete user
        await user1.delete()
        
        # Verify deleted
        deleted = await User.get(user1_id)
        assert deleted is None
        
        # Reinsert with same email (should work)
        user2 = User(
            name="User 2",
            email="reinsert@example.com",
            password_hash="$2b$12$hash2"
        )
        await user2.insert()
        
        assert user2.id is not None
        assert user2.id != user1_id


class TestEmailQueryOperations:
    """Tests for querying by email"""
    
    async def test_find_user_by_email(self, db):
        """Test 13: Find user by unique email"""
        user = User(
            name="Findable User",
            email="findme@example.com",
            password_hash="$2b$12$hash"
        )
        await user.insert()
        
        # Find by email
        found = await User.find_one(User.email == "findme@example.com")
        
        assert found is not None
        assert found.name == "Findable User"
        assert found.email == "findme@example.com"
    
    async def test_find_returns_single_result(self, db):
        """Test 14: Email query returns only one result due to uniqueness"""
        user = User(
            name="Single User",
            email="single@example.com",
            password_hash="$2b$12$hash"
        )
        await user.insert()
        
        # Find all with this email
        results = await User.find(User.email == "single@example.com").to_list()
        
        assert len(results) == 1
        assert results[0].email == "single@example.com"
    
    async def test_count_unique_emails(self, db):
        """Test 15: Count of unique emails equals user count"""
        users = [
            User(
                name=f"User {i}",
                email=f"user{i}@example.com",
                password_hash=f"$2b$12$hash{i}"
            )
            for i in range(10)
        ]
        
        for user in users:
            await user.insert()
        
        total_users = await User.count()
        
        # Get all emails
        all_users = await User.find_all().to_list()
        unique_emails = set(u.email for u in all_users)
        
        assert total_users == 10
        assert len(unique_emails) == 10


class TestEmailNormalizationRecommendations:
    """Tests demonstrating email normalization best practices"""
    
    async def test_lowercase_normalization_prevents_duplicates(self, db):
        """Test 16: Demonstrate lowercase normalization strategy"""
        # Manually normalize emails before insert
        email1 = "User@Example.COM"
        email2 = "user@example.com"
        
        user1 = User(
            name="User 1",
            email=email1.lower(),  # Normalize
            password_hash="$2b$12$hash1"
        )
        await user1.insert()
        
        user2 = User(
            name="User 2",
            email=email2.lower(),  # Normalize
            password_hash="$2b$12$hash2"
        )
        
        # Should fail because both normalize to same email
        with pytest.raises(DuplicateKeyError):
            await user2.insert()

