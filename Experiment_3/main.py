import hashlib
import hmac
import secrets
import time


SHARED_SECRET = b"network_secret_key"
MAX_AGE_SECONDS = 5

pending_challenges = {}
used_nonces = set()


def issue_challenge(username):
    nonce = secrets.token_hex(16)

    pending_challenges[nonce] = (
        username,
        time.time()
    )

    return nonce


def create_response(username, nonce, timestamp=None):

    if timestamp is None:
        timestamp = int(time.time())

    message = f"{username}:{nonce}:{timestamp}".encode()

    tag = hmac.new(
        SHARED_SECRET,
        message,
        hashlib.sha256
    ).hexdigest()

    return timestamp, tag


def verify_response(username, nonce, timestamp, received_tag):

    # Check if nonce was already used
    if nonce in used_nonces:
        return False, "Replay detected: nonce already used"

    # Check whether the challenge exists
    challenge = pending_challenges.get(nonce)

    if challenge is None or challenge[0] != username:
        return False, "Unknown challenge"

    # Check timestamp
    if abs(time.time() - timestamp) > MAX_AGE_SECONDS:

        pending_challenges.pop(nonce, None)
        used_nonces.add(nonce)

        return False, "Expired response"

    # Generate expected HMAC
    message = f"{username}:{nonce}:{timestamp}".encode()

    expected_tag = hmac.new(
        SHARED_SECRET,
        message,
        hashlib.sha256
    ).hexdigest()

    # Compare received and expected HMAC
    valid = hmac.compare_digest(
        received_tag,
        expected_tag
    )

    # Consume the nonce
    pending_challenges.pop(nonce, None)
    used_nonces.add(nonce)

    if valid:
        return True, "Authentication successful"
    else:
        return False, "Authentication failed"


# -------------------- Normal Authentication --------------------

username = "student1"

nonce = issue_challenge(username)

timestamp, tag = create_response(
    username,
    nonce
)

captured = (
    username,
    nonce,
    timestamp,
    tag
)

print("========================================")
print("     Challenge-Response Authentication")
print("========================================")

print("\nNonce:", nonce)
print("Timestamp:", timestamp)
print("HMAC:", tag)

print("\nFirst use:")
print(verify_response(*captured))


# -------------------- Replay Attack --------------------

print("\nReplay:")
print(verify_response(*captured))


# -------------------- Delayed Response --------------------

old_nonce = issue_challenge(username)

old_timestamp = int(time.time()) - 10

old_timestamp, old_tag = create_response(
    username,
    old_nonce,
    old_timestamp
)

print("\nDelayed Response:")
print(
    verify_response(
        username,
        old_nonce,
        old_timestamp,
        old_tag
    )
)
