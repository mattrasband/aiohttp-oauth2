from pathlib import Path
from setuptools import find_packages, setup

__version__ = "0.0.4"

with open(Path(__file__).parent / "README.md") as f:
    long_description = f.read()


setup(
    author="Matt Rasband",
    author_email="matt.rasband@gmail.com",
    description="Provider agnostic OAuth2 client for aiohttp",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["aiohttp"],
    name="aiohttp-oauth2",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7.0",
    setup_requires=["wheel"],
    url="https://github.com/mrasband/aiohttp-oauth2",
    version=__version__,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords=["aiohttp", "oauth2"],
)
