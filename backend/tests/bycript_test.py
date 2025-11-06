""" Application woould crash while hashing password with bcrypt.
Switching to sha256_crypt to verify if hashing works with that scheme.
If this test passes, we can isolate the issue to bcrypt dependency problems.

Conclusion: bcrypt hashing fails, due to conflicts with python 3.13 dependencies.
"""

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

if __name__ == "__main__":
    # Simple test to verify sha256_crypt hashing works
    test_password = "TestPassword123!"
    try:
        hashed = pwd_context.hash(test_password)
        print(f"Password hashed successfully: {hashed}")

        # Verify the password
        if pwd_context.verify(test_password, hashed):
            print("Password verification succeeded.")
        else:
            print("Password verification failed.")
    except Exception as e:
        print(f"Password hashing failed, error: {e}")
