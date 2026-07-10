from setuptools import find_packages, setup
from typing import List


HYPHEN_E_DOT = "-e ."


def get_requirements(file_path: str = "requirements.txt") -> List[str]:
    """
    Read requirements from requirements.txt.
    """

    requirements = []

    with open(file_path) as file:
        requirements = file.readlines()
        requirements = [req.strip() for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="ai_currency_converter",
    version="1.0.0",
    author="Shravan Kumar Pandey",
    author_email="shravankumarpandey825412@gmail.com",
    description="Production Ready AI Currency Converter using Gemini and Exchange Rate API",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.10",
)