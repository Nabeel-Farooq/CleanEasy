from pathlib import Path

from setuptools import find_packages, setup


BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"


setup(
    name="cleaneasy",
    version="0.4.2",
    description="A comprehensive data cleaning toolkit for various data structures",
    long_description=README_PATH.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Aman Sonwani",
    author_email="exehyper999@gmail.com",
    url="https://github.com/CyberMatic-AmAn/cleaneasy",
    license="MIT",
    packages=find_packages(
        exclude=(
            "tests",
            "tests.*",
            "docs",
            "docs.*",
        )
    ),
    include_package_data=True,
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.23.0",
        "scipy>=1.9.0",
        "scikit-learn>=1.1.0",
        "nltk>=3.7",
    ],
    python_requires=">=3.8",
    keywords=[
        "data-cleaning",
        "data-analysis",
        "pandas",
        "machine-learning",
        "data-preprocessing",
    ],
    project_urls={
        "Source": "https://github.com/CyberMatic-AmAn/cleaneasy",
        "Issues": "https://github.com/CyberMatic-AmAn/cleaneasy/issues",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    zip_safe=False,
)
