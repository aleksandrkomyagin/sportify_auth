from base64 import urlsafe_b64encode, urlsafe_b64decode
from functools import lru_cache
from logging import getLogger
from typing import Any

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import (
	RSAPublicNumbers,
	generate_private_key,
)
from cryptography.exceptions import InvalidKey, InvalidSignature, UnsupportedAlgorithm

from sportify_auth.application.dto.rsa_key import RSAKeyDTO
from sportify_auth.infrastructure.exceptions.crypto.rsa_key_generator import PublicKeyGenerationException, RSAGenerationException
from sportify_auth.application.protocols.key_generator.base import IKeyGenerator

logger = getLogger(__name__)



class RSAKeyGenerator(IKeyGenerator):
    async def generate_rsa(self) -> RSAKeyDTO:
        private_key = generate_private_key(public_exponent=65537, key_size=2048)
        try:
            public_key = private_key.public_key()

            private_pem = private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
                # serialization.BestAvailableEncryption(b'password'),
            ).decode("utf-8")

            public_pem = public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode("utf-8")

            numbers = public_key.public_numbers()

            n = urlsafe_b64encode(
                numbers.n.to_bytes((numbers.n.bit_length() + 7) // 8, "big")
            ).rstrip(b"=").decode("utf-8")
            e = urlsafe_b64encode(
                numbers.e.to_bytes((numbers.e.bit_length() + 7) // 8, "big")
            ).rstrip(b"=").decode("utf-8")
        except (UnsupportedAlgorithm, InvalidKey, InvalidSignature, ValueError, TypeError, Exception) as e:
            logger.error("Ошибка генерации RSA: %s", str(e))
            raise RSAGenerationException(message="Ошибка генерации RSA") from e

        return RSAKeyDTO(
            private_pem=private_pem,
            public_pem=public_pem,
            n=n,
            e=e,
        )

    async def generate_public_key_from_jwk(self, jwk: dict[str, Any]) -> str:
        try:
            n = int.from_bytes(urlsafe_b64decode(jwk["n"] + "=="), byteorder="big")
            e = int.from_bytes(urlsafe_b64decode(jwk["e"] + "=="), byteorder="big")
            pub_numbers = RSAPublicNumbers(e, n)
            public_key = pub_numbers.public_key(default_backend())
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()
        except (UnsupportedAlgorithm, InvalidKey, InvalidSignature, ValueError, TypeError, Exception) as e:
            logger.error("Ошибка генерации публичного ключа RSA: %s", str(e))
            raise PublicKeyGenerationException(message="Ошибка генерации публичного ключа RSA") from e
        return public_key_pem


@lru_cache
def get_rsa_key_generator() -> RSAKeyGenerator:
    return RSAKeyGenerator()
