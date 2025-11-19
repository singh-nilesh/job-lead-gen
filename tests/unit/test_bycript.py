import pytest
from passlib.context import CryptContext

@pytest.fixture(scope="module")
def pwd_context():
    return CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def test_sha256_crypt_hashing_basic(pwd_context):
    """Check if hashing works correctly for sha256_crypt."""
    password = "TestPassword123!"
    hashed = pwd_context.hash(password)

    # Basic sanity checks
    assert isinstance(hashed, str)
    assert hashed != password
    assert pwd_context.identify(hashed) == "sha256_crypt"
    assert pwd_context.verify(password, hashed)


def test_verify_rejects_wrong_password(pwd_context):
    """Check if verification fails for incorrect password."""
    hashed = pwd_context.hash("correct-horse-battery-staple")
    assert not pwd_context.verify("incorrect-password", hashed)


def test_same_password_produces_different_hashes_but_both_verify(pwd_context):
    """Check if the same password produces different hashes but both verify correctly."""
    pw = "reused-password"
    h1 = pwd_context.hash(pw)
    h2 = pwd_context.hash(pw)
    # Salted hashes should differ but both should verify the original password
    assert h1 != h2
    assert pwd_context.verify(pw, h1)
    assert pwd_context.verify(pw, h2)
