from setuptools import setup, find_packages

setup(
    name="prudentia-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "prudentia=prudentia_cli.cli:cli",
        ],
    },
    python_requires=">=3.6",
    author="Prudentia Sciences",
    author_email="dev@prudentia.com",
    description="CLI tool for Prudentia internal developers",
    keywords="prudentia, cli, development",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
) 