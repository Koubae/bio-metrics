import pytest
from src.auth.infrastructure.access_token import HashLibPasswordHasher


class TestHashLibPasswordHasher:

    def test_hash_password_generates_consistent_hash(self):
        password = "test_password"
        hashed_password1 = HashLibPasswordHasher.hash_password(password)
        hashed_password2 = HashLibPasswordHasher.hash_password(password)
        assert hashed_password1 == hashed_password2, "Hashing the same password should produce consistent results"

    def test_hash_password_generates_different_hashes_for_different_inputs(self):
        password1 = "password_one"
        password2 = "password_two"
        hashed_password1 = HashLibPasswordHasher.hash_password(password1)
        hashed_password2 = HashLibPasswordHasher.hash_password(password2)
        assert hashed_password1 != hashed_password2, "Hashing different passwords should produce different results"

    def test_verify_password_with_matching_password(self):
        password = "secure_password"
        hashed_password = HashLibPasswordHasher.hash_password(password)
        result = HashLibPasswordHasher.verify_password(password, hashed_password)
        assert result is True, "verify_password should return True for matching password and hash"

    def test_verify_password_with_non_matching_password(self):
        password = "secure_password"
        hashed_password = HashLibPasswordHasher.hash_password(password)
        fake_password = "fake_password"
        result = HashLibPasswordHasher.verify_password(fake_password, hashed_password)
        assert result is False, "verify_password should return False for non-matching password and hash"
