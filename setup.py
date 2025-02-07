import distutils.cmd
import os
import subprocess

from setuptools import find_packages, setup


class BaseCommand(distutils.cmd.Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass


def create_command(text, commands):
    """Creates a custom setup.py command."""

    class CustomCommand(BaseCommand):
        description = text

        def run(self):
            for cmd in commands:
                subprocess.check_call(cmd)

    return CustomCommand


with open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as readme:
    README = readme.read().split("h1>\n", 2)[1]


setup(
    name="django-postgres-extra",
    version="2.0.3rc3",
    packages=find_packages(),
    include_package_data=True,
    license="MIT License",
    description="Bringing all of PostgreSQL's awesomeness to Django.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/SectorLabs/django-postgres-extra",
    author="Sector Labs",
    author_email="open-source@sectorlabs.ro",
    keywords=["django", "postgres", "extra", "hstore", "ltree"],
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires=">=3.6",
    install_requires=[
        "Django>=2.0",
        "enforce>=0.3.4,<=1.0.0",
        "python-dateutil>=2.8.0,<=3.0.0",
        "structlog>=19,<23.0.0",
        "ansimarkup>=1.4.0,<=2.0.0",
    ],
    extras_require={
        ':python_version <= "3.6"': ["dataclasses"],
        "docs": ["Sphinx==2.2.0", "sphinx-rtd-theme==0.4.3"],
        "test": [
            "psycopg2>=2.8.4,<3.0.0",
            "dj-database-url==0.5.0",
            "pytest==5.3.2",
            "pytest-benchmark==3.2.2",
            "pytest-django==3.7.0",
            "pytest-cov==2.8.1",
            "tox==3.14.0",
            "freezegun==0.3.12",
            "coveralls==1.10.0",
            "snapshottest==0.5",
        ],
        "analysis": [
            "black==19.3b0",
            "flake8==3.7.7",
            "autoflake==1.3",
            "autopep8==1.4.4",
            "isort==4.3.20",
            "sl-docformatter==1.4",
        ],
    },
    cmdclass={
        "lint": create_command(
            "Lints the code", [["flake8", "setup.py", "psqlextra", "tests"]]
        ),
        "lint_fix": create_command(
            "Lints the code",
            [
                [
                    "autoflake",
                    "--remove-all-unused-imports",
                    "-i",
                    "-r",
                    "setup.py",
                    "psqlextra",
                    "tests",
                ],
                ["autopep8", "-i", "-r", "setup.py", "psqlextra", "tests"],
            ],
        ),
        "format": create_command(
            "Formats the code", [["black", "setup.py", "psqlextra", "tests"]]
        ),
        "format_verify": create_command(
            "Checks if the code is auto-formatted",
            [["black", "--check", "setup.py", "psqlextra", "tests"]],
        ),
        "format_docstrings": create_command(
            "Auto-formats doc strings", [["docformatter", "-r", "-i", "."]]
        ),
        "format_docstrings_verify": create_command(
            "Verifies that doc strings are properly formatted",
            [["docformatter", "-r", "-c", "."]],
        ),
        "sort_imports": create_command(
            "Automatically sorts imports",
            [
                ["isort", "setup.py"],
                ["isort", "-rc", "psqlextra"],
                ["isort", "-rc", "tests"],
            ],
        ),
        "sort_imports_verify": create_command(
            "Verifies all imports are properly sorted.",
            [
                ["isort", "-c", "setup.py"],
                ["isort", "-c", "-rc", "psqlextra"],
                ["isort", "-c", "-rc", "tests"],
            ],
        ),
        "fix": create_command(
            "Automatically format code and fix linting errors",
            [
                ["python", "setup.py", "format"],
                ["python", "setup.py", "format_docstrings"],
                ["python", "setup.py", "sort_imports"],
                ["python", "setup.py", "lint_fix"],
                ["python", "setup.py", "lint"],
            ],
        ),
        "verify": create_command(
            "Verifies whether the code is auto-formatted and has no linting errors",
            [
                ["python", "setup.py", "format_verify"],
                ["python", "setup.py", "format_docstrings_verify"],
                ["python", "setup.py", "sort_imports_verify"],
                ["python", "setup.py", "lint"],
            ],
        ),
        "test": create_command(
            "Runs all the tests",
            [
                [
                    "pytest",
                    "--cov=psqlextra",
                    "--cov-report=term",
                    "--cov-report=xml:reports/xml",
                    "--cov-report=html:reports/html",
                    "--junitxml=reports/junit/tests.xml",
                    "--reuse-db",
                ]
            ],
        ),
    },
)
