import os
import sys
from typing import Dict
from click import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def format_db_url(
    dbhost: str,
    dbusername: str,
    dbpassword: str,
    dbname: str,
):
    return f"mysql://{dbusername}:{dbpassword}@{dbhost}:3306/{dbname}"


DEBUG_ENV_VAR = "DEBUG"
SSL_CERT_ENV_VAR = "DB_SSL_CERT_PATH"
ENABLE_TLS_ENV_VAR = "ENABLE_TLS_SUPPORT"

DEBUG = bool(os.environ.get(DEBUG_ENV_VAR, "").lower() == "true")
ENABLE_TLS = bool(os.environ.get(ENABLE_TLS_ENV_VAR, "true").lower() == "true")


def get_ssl_settings() -> Dict[str, Dict[str, str | bool]]:
    """
    Get SSL settings used for database TLS connection if available.

    Returns:
        A dict containing the required connection's SSL settings.

    Raises:
        FileNotFoundError: If the SSL certificate path is invalid.
        TypeError: If the SSL certificate path is not found in environment variables.
    """
    if "pytest" in " ".join(sys.argv) or DEBUG or not ENABLE_TLS:
        return {}

    ssl_cert_path = os.environ.get(SSL_CERT_ENV_VAR)
    if not ssl_cert_path:
        raise TypeError(
            f"Path to SSL certificate not found in environment variable {SSL_CERT_ENV_VAR}"
        )

    ssl_cert = Path(ssl_cert_path)

    if not ssl_cert.is_file():
        raise FileNotFoundError(
            f"Incorrect SSL certificate path. Path is not a file: {ssl_cert}"
        )

    return {"ssl": {"ca": str(ssl_cert), "verify_cert": True, "check_hostname": True}}

def create_database_engine(db_url=None):
    if not db_url:
        DB_USERNAME = os.environ.get("DB_USERNAME", "")
        DB_HOSTNAME = os.environ.get("DB_HOSTNAME", "")
        DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
        LPR_DB_NAME = os.environ.get("LPR_DB_NAME", "lprdb")

        db_url = format_db_url(
            dbhost=DB_HOSTNAME,
            dbusername=DB_USERNAME,
            dbpassword=DB_PASSWORD,
            dbname=LPR_DB_NAME,
        )

    ssl_settings = get_ssl_settings()

    return create_engine(
        url=db_url,
        connect_args={"connect_timeout": 2, **ssl_settings},
        isolation_level="READ COMMITTED",
        pool_pre_ping=1,
        echo=True if os.getenv("DB_LOG_LEVEL", "ERROR") == "DEBUG" else False,
        pool_timeout=3,
        enable_from_linting=False,
        query_cache_size=0,
    )

