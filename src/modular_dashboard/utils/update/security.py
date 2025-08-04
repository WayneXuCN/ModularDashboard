"""Security validation mechanisms for module updates."""

import hashlib
import os
from pathlib import Path

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from loguru import logger

from .core import UpdateValidator


class ChecksumValidator(UpdateValidator):
    """Validator for file checksums."""

    def __init__(self):
        self.supported_algorithms = {
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512,
            "md5": hashlib.md5,
        }

    async def verify_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify file checksum."""
        try:
            # Parse checksum (format: algorithm:hash)
            if ":" in expected_checksum:
                algorithm, hash_value = expected_checksum.split(":", 1)
            else:
                # Default to SHA256
                algorithm = "sha256"
                hash_value = expected_checksum

            if algorithm not in self.supported_algorithms:
                logger.error(f"Unsupported checksum algorithm: {algorithm}")
                return False

            # Calculate file checksum
            actual_hash = await self._calculate_checksum(file_path, algorithm)

            # Compare (case-insensitive for hex)
            return actual_hash.lower() == hash_value.lower()

        except Exception as e:
            logger.error(f"Error verifying checksum: {e}")
            return False

    async def verify_signature(self, file_path: str, signature: str) -> bool:
        """Checksum validator doesn't support signatures."""
        logger.warning("Checksum validator doesn't support signature verification")
        return True

    async def _calculate_checksum(self, file_path: str, algorithm: str) -> str:
        """Calculate checksum for a file."""
        hash_func = self.supported_algorithms[algorithm]()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_func.update(chunk)

        return hash_func.hexdigest()


class SignatureValidator(UpdateValidator):
    """Validator for digital signatures."""

    def __init__(self, public_keys: dict[str, str]):
        """Initialize with public keys.

        Args:
            public_keys: Dictionary mapping key IDs to public key PEM strings
        """
        self.public_keys = {}
        self._load_public_keys(public_keys)

    def _load_public_keys(self, public_keys: dict[str, str]) -> None:
        """Load public keys from PEM strings."""
        for key_id, pem_key in public_keys.items():
            try:
                public_key = serialization.load_pem_public_key(
                    pem_key.encode(), backend=default_backend()
                )
                self.public_keys[key_id] = public_key
            except Exception as e:
                logger.error(f"Error loading public key {key_id}: {e}")

    async def verify_signature(self, file_path: str, signature: str) -> bool:
        """Verify file signature."""
        try:
            # Parse signature (format: key_id:signature)
            if ":" in signature:
                key_id, signature_data = signature.split(":", 1)
            else:
                # Use default key
                key_id = "default"
                signature_data = signature

            if key_id not in self.public_keys:
                logger.error(f"Unknown public key ID: {key_id}")
                return False

            public_key = self.public_keys[key_id]

            # Decode signature from base64
            import base64

            signature_bytes = base64.b64decode(signature_data)

            # Calculate file hash
            file_hash = await self._calculate_file_hash(file_path)

            # Verify signature
            public_key.verify(
                signature_bytes,
                file_hash,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH,
                ),
                hashes.SHA256(),
            )

            return True

        except InvalidSignature:
            logger.error("Invalid signature")
            return False
        except Exception as e:
            logger.error(f"Error verifying signature: {e}")
            return False

    async def verify_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Signature validator doesn't support checksum verification."""
        logger.warning("Signature validator doesn't support checksum verification")
        return True

    async def _calculate_file_hash(self, file_path: str) -> bytes:
        """Calculate SHA256 hash of file."""
        sha256_hash = hashlib.sha256()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256_hash.update(chunk)

        return sha256_hash.digest()


class CompositeValidator(UpdateValidator):
    """Composite validator that combines multiple validation strategies."""

    def __init__(self, validators: list[UpdateValidator]):
        """Initialize with list of validators."""
        self.validators = validators

    async def verify_signature(self, file_path: str, signature: str) -> bool:
        """Verify signature using all validators."""
        results = []

        for validator in self.validators:
            try:
                result = await validator.verify_signature(file_path, signature)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in signature validator: {e}")
                results.append(False)

        # All validators must pass
        return all(results)

    async def verify_checksum(self, file_path: str, expected_checksum: str) -> bool:
        """Verify checksum using all validators."""
        results = []

        for validator in self.validators:
            try:
                result = await validator.verify_checksum(file_path, expected_checksum)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in checksum validator: {e}")
                results.append(False)

        # All validators must pass
        return all(results)


class KeyManager:
    """Manages cryptographic keys for update validation."""

    def __init__(self, keys_dir: str):
        self.keys_dir = Path(keys_dir)
        self.keys_dir.mkdir(parents=True, exist_ok=True)

        self.public_keys: dict[str, str] = {}
        self.private_keys: dict[str, str] = {}

        self._load_keys()

    def _load_keys(self) -> None:
        """Load keys from the keys directory."""
        # Load public keys
        public_keys_dir = self.keys_dir / "public"
        if public_keys_dir.exists():
            for key_file in public_keys_dir.glob("*.pem"):
                try:
                    with open(key_file) as f:
                        key_id = key_file.stem
                        self.public_keys[key_id] = f.read()
                except Exception as e:
                    logger.error(f"Error loading public key {key_file}: {e}")

        # Load private keys
        private_keys_dir = self.keys_dir / "private"
        if private_keys_dir.exists():
            for key_file in private_keys_dir.glob("*.pem"):
                try:
                    with open(key_file) as f:
                        key_id = key_file.stem
                        self.private_keys[key_id] = f.read()
                except Exception as e:
                    logger.error(f"Error loading private key {key_file}: {e}")

    def generate_key_pair(self, key_id: str, key_size: int = 2048) -> tuple[str, str]:
        """Generate a new RSA key pair."""
        try:
            # Generate private key
            private_key = rsa.generate_private_key(
                public_exponent=65537, key_size=key_size, backend=default_backend()
            )

            # Get public key
            public_key = private_key.public_key()

            # Serialize keys
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            ).decode()

            public_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()

            # Save keys
            self._save_key_pair(key_id, private_pem, public_pem)

            return private_pem, public_pem

        except Exception as e:
            logger.error(f"Error generating key pair: {e}")
            raise

    def _save_key_pair(self, key_id: str, private_pem: str, public_pem: str) -> None:
        """Save key pair to files."""
        try:
            # Save private key
            private_key_path = self.keys_dir / "private" / f"{key_id}.pem"
            private_key_path.parent.mkdir(parents=True, exist_ok=True)
            with open(private_key_path, "w") as f:
                f.write(private_pem)

            # Save public key
            public_key_path = self.keys_dir / "public" / f"{key_id}.pem"
            public_key_path.parent.mkdir(parents=True, exist_ok=True)
            with open(public_key_path, "w") as f:
                f.write(public_pem)

            # Update in-memory keys
            self.private_keys[key_id] = private_pem
            self.public_keys[key_id] = public_pem

            logger.info(f"Key pair {key_id} saved successfully")

        except Exception as e:
            logger.error(f"Error saving key pair {key_id}: {e}")
            raise

    def get_public_key(self, key_id: str) -> str | None:
        """Get public key by ID."""
        return self.public_keys.get(key_id)

    def get_private_key(self, key_id: str) -> str | None:
        """Get private key by ID."""
        return self.private_keys.get(key_id)

    def list_public_keys(self) -> list[str]:
        """List all public key IDs."""
        return list(self.public_keys.keys())

    def create_validator(self, key_ids: list[str] | None = None) -> SignatureValidator:
        """Create a signature validator with specified keys."""
        if key_ids is None:
            # Use all available public keys
            keys_to_use = self.public_keys
        else:
            # Use only specified keys
            keys_to_use = {k: v for k, v in self.public_keys.items() if k in key_ids}

        return SignatureValidator(keys_to_use)


class SecurityValidator:
    """Main security validator that coordinates all validation."""

    def __init__(
        self,
        keys_dir: str,
        require_signature: bool = True,
        require_checksum: bool = True,
    ):
        self.keys_dir = keys_dir
        self.require_signature = require_signature
        self.require_checksum = require_checksum

        # Initialize components
        self.key_manager = KeyManager(keys_dir)
        self.checksum_validator = ChecksumValidator()
        self.signature_validator = self.key_manager.create_validator()

        # Create composite validator
        validators = []
        if require_checksum:
            validators.append(self.checksum_validator)
        if require_signature:
            validators.append(self.signature_validator)

        self.validator = CompositeValidator(validators)

    async def validate_update(
        self, file_path: str, checksum: str = "", signature: str = ""
    ) -> bool:
        """Validate an update package."""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"Update file not found: {file_path}")
                return False

            # Validate checksum if required
            if self.require_checksum and checksum:
                if not await self.validator.verify_checksum(file_path, checksum):
                    logger.error("Checksum validation failed")
                    return False
            elif self.require_checksum and not checksum:
                logger.warning("Checksum required but not provided")

            # Validate signature if required
            if self.require_signature and signature:
                if not await self.validator.verify_signature(file_path, signature):
                    logger.error("Signature validation failed")
                    return False
            elif self.require_signature and not signature:
                logger.warning("Signature required but not provided")

            return True

        except Exception as e:
            logger.error(f"Error validating update: {e}")
            return False

    def generate_key_pair(self, key_id: str, key_size: int = 2048) -> tuple[str, str]:
        """Generate a new key pair for signing updates."""
        return self.key_manager.generate_key_pair(key_id, key_size)

    def list_available_keys(self) -> list[str]:
        """List all available public keys."""
        return self.key_manager.list_public_keys()

    def get_public_key_pem(self, key_id: str) -> str | None:
        """Get public key in PEM format."""
        return self.key_manager.get_public_key(key_id)
