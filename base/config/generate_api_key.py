import secrets
import uuid
import logging

# Set up console logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_api_key():
    """
    Generates a secure, unique API key.
    Format: "key_" + UUID + random token
    """
    part1 = str(uuid.uuid4())
    part2 = secrets.token_urlsafe(16)  # 128-bit entropy
    api_key = f"key_{part1}_{part2}"

    with open(
        "/home/prince/PycharmProjects/FastApiProjects/FastCRUD/.env", "a"
    ) as env_file:
        env_file.write(f"\nAPI_KEY={api_key}\n")

    return api_key


if __name__ == "__main__":
    api_key = generate_api_key()
    logger.info(
        f"✅ New API Key generated:\n\n🔐 {api_key}\n\n⚠️ Store it securely. This will not be shown again."
    )
