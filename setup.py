from setuptools import setup, find_packages

setup(
    name="flowcompiler",
    version="1.2.3",
    author="Srijan Sundaram",
    author_email="srijansundram@gmail.com",
    description="A lightweight data pipeline compiler with syntax validation, AI suggestions, and CLI integration.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/srijansundaram/FlowCompiler",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pandas>=2.0.0",
        "rich>=13.0.0"
    ],
    entry_points={
        "console_scripts": [
            "flowc=flowc.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Compilers",
    ],
    python_requires=">=3.8",
)
