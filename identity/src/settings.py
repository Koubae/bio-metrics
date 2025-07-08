import os
import sys
import typing as t
from dataclasses import dataclass, field

from src.auth.domain.exceptions import AuthCertificateLoadException


@dataclass(frozen=True)
class Settings:
    """Singleton Instance for Application settings"""

    _singleton: t.ClassVar[t.Optional["Settings"]] = None

    ROOT_PATH: t.ClassVar[str] = os.path.dirname(os.path.abspath(__file__))
    CONF_PATH: t.ClassVar[str] = os.path.join(ROOT_PATH, "..", "conf")
    TESTS_PATH: t.ClassVar[str] = os.path.join(ROOT_PATH, "..", "tests")

    # ----------------------------
    #   App
    # ----------------------------
    log_level: str
    log_format: str
    app_name: str
    app_version: str
    app_api_cors_allowed_domains: tuple[str, ...]
    app_jwt_expiration_hours: int

    # ----------------------------
    #   Database
    # ----------------------------
    db_name: str | None
    db_host: str | None
    db_port: int | None
    db_user: str | None
    db_password: str | None

    db_pool_size: int
    db_max_overflow: int
    db_pool_recycle: int
    db_pool_pre_ping: bool
    db_echo: bool

    cert_private_file_name: str | None = field(repr=False)
    cert_public_file_name: str | None = field(repr=False)

    cert_private: str | None = field(default=None, repr=False)
    cert_public: str | None = field(default=None, repr=False)

    @classmethod
    def get(cls) -> "Settings":
        if cls._singleton is None:
            cert_private_file_name = os.getenv("APP_CERT_PRIVATE_FILE_NAME", None)
            cert_public_file_name = os.getenv("APP_CERT_PUBLIC_FILE_NAME", None)
            cert_private, cert_public = cls._load_certificates(cert_private_file_name, cert_public_file_name)
            app_jwt_expiration_hours = min(int(os.getenv("APP_JWT_EXPIRATION_HOURS", 4)), 1)

            cls._singleton = cls(
                app_jwt_expiration_hours=app_jwt_expiration_hours,
                log_level=os.getenv("LOG_LEVEL", "DEBUG"),
                log_format=os.getenv("LOG_FORMAT", "%(asctime)s %(message)s"),
                app_name=os.getenv("APP_NAME", "Jabba AI-Bot"),
                app_version=os.getenv("APP_VERSION", "undefined"),
                app_api_cors_allowed_domains=tuple(os.environ.get("APP_API_CORS_ALLOWED_DOMAINS", "").split(",")),

                db_name=os.getenv("DB_NAME", None),
                db_host=os.getenv("DB_HOST", "localhost"),
                db_port=int(os.getenv("DB_PORT", 5432)),
                db_user=os.getenv("DB_USER", None),
                db_password=os.getenv("DB_PASS", None),
                db_pool_size=int(os.getenv("DB_POOL_SIZE", 5)),
                db_max_overflow=int(os.getenv("DB_MAX_OVERFLOW", 10)),
                db_pool_recycle=int(os.getenv("DB_POOL_RECYCLE", -1)),
                db_pool_pre_ping=cls.parse_bool_env("DB_POOL_PRE_PING", True),
                db_echo=cls.parse_bool_env("DB_ECHO", False),

                cert_private_file_name=cert_private_file_name,
                cert_public_file_name=cert_public_file_name,
                cert_private=cert_private,
                cert_public=cert_public,

            )
        return cls._singleton

    def get_app_info(self) -> str:
        info = f"{self.app_name} V{self.app_version}!"
        return info

    def get_cert_public(self) -> str:
        return self.cert_public

    def get_cert_private(self) -> str:
        return self.cert_private

    @staticmethod
    def parse_bool_env(env_name: str, default: bool = False) -> bool:
        return os.getenv(env_name, str(default)).lower() in ("true", "1")

    @classmethod
    def _load_certificates(cls, cert_private_file_name: str | None, cert_public_file_name: str | None) -> tuple[
        str | None, str | None]:
        cert_private: str | None = None
        cert_public: str | None = None

        cert_private_file_name = cert_private_file_name.strip() if cert_private_file_name else None
        cert_public_file_name = cert_public_file_name.strip() if cert_public_file_name else None

        if cert_private_file_name:
            cert_private = cls._load_cert(cert_private_file_name)
        if cert_public_file_name:
            cert_public = cls._load_cert(cert_public_file_name)
        return cert_private, cert_public

    @classmethod
    def _load_cert(cls, cert_file_name: str) -> str:
        try:
            with open(os.path.join(cls.CONF_PATH, cert_file_name), "r") as f:
                certificate = f.read()
        except (FileNotFoundError, PermissionError, UnicodeError) as error:
            print(f"Error loading certificate file: {error}", file=sys.stderr)
            raise AuthCertificateLoadException(f"Could not load certificate file {cls}: {error}") from error

        certificate = certificate.strip()
        if not certificate:
            raise AuthCertificateLoadException(f"Certificate file {cert_file_name} is empty")
        return certificate
