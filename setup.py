from setuptools import find_packages, setup

MAJOR = 1
MINOR = 0
PATCH = 0

PACKAGE_NAME = "maine=lpr-db-models"

setup(
    name=PACKAGE_NAME,
    version=f"{MAJOR}.{MINOR}.{PATCH}",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy>=2.0.0",
        "alembic>=1.12.0",
    ],
)
