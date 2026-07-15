"""Password hashing utilities.

Real systems never store passwords in plain text. This module hashes every
password with PBKDF2-HMAC-SHA256 and a unique random salt per user, using
only the Python standard library (no extra dependencies to install).
"""

import hashlib
import hmac
import os

_ALGORITHM = "sha256"
_ITERATIONS = 200_000
_SALT_BYTES = 16


def hash_password(raw_password):
    """Hash a raw password with a fresh random salt.

    Returns a single string ``"<salt_hex>$<hash_hex>"`` that is safe to
    persist to disk. The same password hashed twice produces two different
    strings because the salt is random each time.
    """
    salt = os.urandom(_SALT_BYTES)
    digest = hashlib.pbkdf2_hmac(
        _ALGORITHM, raw_password.encode("utf-8"), salt, _ITERATIONS
    )
    return f"{salt.hex()}${digest.hex()}"


def verify_password(raw_password, stored_hash):
    """Check a raw password against a stored ``"<salt_hex>$<hash_hex>"`` value.

    Uses a constant-time comparison so response timing cannot leak how much
    of the hash matched. Malformed stored data returns False instead of
    raising, so a corrupted record fails closed rather than crashing login.
    """
    try:
        salt_hex, digest_hex = str(stored_hash).split("$", 1)
        salt = bytes.fromhex(salt_hex)
    except (ValueError, AttributeError):
        return False
    candidate = hashlib.pbkdf2_hmac(
        _ALGORITHM, raw_password.encode("utf-8"), salt, _ITERATIONS
    )
    return hmac.compare_digest(candidate.hex(), digest_hex)
