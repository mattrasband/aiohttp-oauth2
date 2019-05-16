from setuptools import find_packages, setup

__version__ = "0.0.1"


setup(
    author="Matt Rasband",
    author_email="matt.rasband@gmail.com",
    description="Provider agnostic OAuth2 client for aiohttp",
    install_requires=["aiohttp"],
    name="aiohttp-oauth2",
    packages=find_packages(exclude=["tests"]),
    python_requires=">=3.7.0",
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
